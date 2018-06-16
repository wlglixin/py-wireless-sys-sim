import numpy as np


def cal_channel_gain(tr, rv, n, n_channel,
                     dist_func=None, dist_args=[],
                     pl_func=None, pl_args=[],
                     fading_func=None, fading_args=[],
                     shadowing_func=None, shadowing_args=[]):
    d = dist_func(tr, rv, *dist_args)
    pl = pl_func(d, *pl_args)
    fading_args = fading_args + [n, n_channel] if n_channel > 1 else fading_args + [n]
    h = fading_func(*fading_args)
    shadowing_args = shadowing_args + [n]
    s = shadowing_func(*shadowing_args)
    return np.kron(10**((-pl+s)/10.0), np.ones(n_channel)) * (abs(h)**2)


def cal_recv_power(tr, rv, tp, n, n_channel,
                   dist_func, dist_args,
                   pl_func, pl_args,
                   fading_func, fading_args,
                   shadowing_func, shadowing_args):
    if not (n_channel == 1 or
            (hasattr(tp, '__len__') and len(tp) == n_channel)):
        tp = np.kron(tp, np.ones(n_channel))
    return tp * cal_channel_gain(tr, rv, n, n_channel,
                                 dist_func, dist_args,
                                 pl_func, pl_args,
                                 fading_func, fading_args,
                                 shadowing_func, shadowing_args)


def cal_thermal_noise(bw, t):
    K = 1.3806488e-23
    return bw*t*K


def cal_SINR(sp, ip, noise):
    """
    Args:
    sp (float or numpy array): signal power
    ip (float or numpy array): interference power
    """
    return sp / (ip+noise)


def cal_shannon_cap(bw, sp, ip, noise):
    sinr = cal_SINR(sp, ip, noise)
    return bw * np.log2(1+sinr)


def cal_transmission_time(throughput, packet=1e3, period=1e-3):
    """
    Args:
    throughput (float): bps
    packet (float): bits
    period (float): time slot (s)

    Return:
    Total transmission time (float): in s
    """
    pass
