from torch.optim.lr_scheduler import _LRScheduler

from colossalai.registry import LR_SCHEDULERS


@LR_SCHEDULERS.register_module
class LinearWarmupLR(_LRScheduler):
    """Linearly warmup learning rate and then linearly decay

    :param optimizer: Wrapped optimizer
    :type optimizer: torch.optim.Optimizer
    :param total_steps: number of total training steps
    :type total_steps: int
    :param warmup_steps: number of warmup steps, defaults to 0
    :type warmup_steps: int, optional
    :param last_epoch: The index of last epoch, defaults to -1
    :type last_epoch: int, optional
    """

    def __init__(self, optimizer, total_steps: int, warmup_steps: int = 0, last_epoch: int = -1, **kwargs):
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps
        super().__init__(optimizer, last_epoch=last_epoch)

    def get_lr(self):
        if self.last_epoch < self.warmup_steps:
            return [(self.last_epoch + 1) / (self.warmup_steps + 1) * lr for lr in self.base_lrs]
        else:
            return [(self.total_steps - self.last_epoch) / (self.total_steps - self.warmup_steps) * lr for lr in
                    self.base_lrs]


@LR_SCHEDULERS.register_module
class LinearWarmupDecay(_LRScheduler):
    def __init__(self, optimizer, total_steps: int, warmup_steps: int = 0, last_epoch: int = -1, **kwargs):
        self.warmup_steps = int(warmup_steps)
        self.total_steps = total_steps
        super().__init__(optimizer, last_epoch=last_epoch)

    def get_lr(self):
        if self.last_epoch < self.warmup_steps:
            return [(self.last_epoch + 1) / self.warmup_steps * lr for lr in self.base_lrs]
        else:
            return [(self.total_steps - self.last_epoch - 1) / (self.total_steps - self.warmup_steps) * lr for lr in
                    self.base_lrs]
