from base.base_train import BaseTrain
from tqdm import tqdm
import numpy as np

class RNNTrainer(BaseTrain):
    def __init__(self,sess,model,data,config,logger):
        super(RNNTrainer, self).__init__(sess,model,data,config,logger)

    def train_epoch(self):
        self.state = np.zeros((self.config.lstm_layers, 2, self.config.batch_size, self.config.hidden_size))
        loop = tqdm(range(self.config.num_iter_per_epoch))
        losses = []
        for _ in loop:
            loss = self.train_step()
            losses.append(loss)
        loss = np.mean(losses)

        cur_it = self.model.global_step_tensor.eval(self.sess)
        summaries_dict = {
            'loss': loss,
        }
        self.logger.summarize(cur_it, summaries_dict=summaries_dict)
        self.model.save(self.sess)

    def train_step(self):
        time_slice, batch_x, batch_y = next(self.data.next_batch())
        if time_slice == 0:
            self.state = np.zeros((self.config.lstm_layers, 2, self.config.batch_size, self.config.hidden_size))
        feed_dict = {self.model.x: batch_x, self.model.y: batch_y, self.model.is_training: True, self.model.batch_size: self.config.batch_size, self.model.init_state: self.state}
        _, loss, self.state = self.sess.run([self.model.train_step, self.model.cross_entropy, self.model.init_state], feed_dict=feed_dict)
        return loss
