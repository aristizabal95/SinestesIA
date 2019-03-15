from base.base_train import BaseTrain
from tqdm import tqdm
import numpy as np

class CAETrainer(BaseTrain):
    def __init__(self,sess,model,data,config,logger):
        super(CAETrainer, self).__init__(sess,model,data,config,logger)

    def train_epoch(self):
        loop = tqdm(range(self.config.num_iter_per_epoch))
        losses = []
        for _ in loop:
            loss, input, expected, encoded, decoded, acc = self.train_step()
            losses.append(loss)
        loss = np.mean(losses)

        cur_it = self.model.global_step_tensor.eval(self.sess)
        summaries_dict = {
            'loss': loss,
            'input': input,
            '0.expected': expected,
            '1.decoded': decoded,
            '2.encoded': encoded,
            'accuracy': acc
        }
        self.logger.summarize(cur_it, summaries_dict=summaries_dict)
        self.model.save(self.sess)

    def train_step(self):
        batch_x, batch_y = next(self.data.next_batch(self.config.batch_size))
        feed_dict = {self.model.x: batch_x, self.model.y: batch_y, self.model.is_training: True}
        _, loss = self.sess.run([self.model.train_step, self.model.cross_entropy], feed_dict=feed_dict)
        input, expected = next(self.data.cv_batch())
        encoding, pred, accuracy = self.sess.run([self.model.encoded, self.model.decoded, self.model.cross_entropy], feed_dict={self.model.x: input, self.model.y: expected})
        encoding = np.reshape(encoding,(-1,16,8,4))
        return loss, input, expected, encoding, pred, accuracy
