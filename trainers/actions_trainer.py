from base.base_train import BaseTrain
from tqdm import tqdm
import numpy as np

class ActionsTrainer(BaseTrain):
    def __init__(self,sess,model,data,config,logger):
        super(ActionsTrainer, self).__init__(sess,model,data,config,logger)

    def train_epoch(self):
        loop = tqdm(range(self.config.num_iter_per_epoch))
        losses = []
        for _ in loop:
            loss, acc = self.train_step()
            losses.append(loss)
        loss = np.mean(losses)

        cur_it = self.model.global_step_tensor.eval(self.sess)
        summaries_dict = {
            'loss': loss,
            'accuracy': acc
        }
        self.logger.summarize(cur_it, summaries_dict=summaries_dict)
        self.model.save(self.sess)

    def train_step(self):
        batch_x, batch_y = next(self.data.next_batch(self.config.batch_size))
        feed_dict = {self.model.x: batch_x, self.model.y: batch_y, self.model.is_training: True}
        _, loss = self.sess.run([self.model.train_step, self.model.cross_entropy], feed_dict=feed_dict)
        cv_x, cv_y = next(self.data.cv_batch(100))
        acc = self.sess.run(self.model.cross_entropy, feed_dict={self.model.x: cv_x, self.model.y: cv_y})
        return loss, acc
