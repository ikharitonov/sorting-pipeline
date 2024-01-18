import numpy as np

# Taken from https://github.com/int-brain-lab/ibl-neuropixel/blob/main/src/neuropixel.py#L146
def adc_shifts(version=1, nc=384):
    """
    Neuropixel NP1
    The sampling is serial within the same ADC, but it happens at the same time in all ADCs.
    The ADC to channel mapping is done per odd and even channels:
    ADC1: ch1, ch3, ch5, ch7...
    ADC2: ch2, ch4, ch6....
    ADC3: ch33, ch35, ch37...
    ADC4: ch34, ch36, ch38...
    Therefore, channels 1, 2, 33, 34 get sample at the same time. I hope this is more or
    less clear. In 1.0, it is similar, but there we have 32 ADC that sample each 12 channels."
    - Nick on Slack after talking to Carolina - ;-)

    There are 384 channels (each with AP and LFP) divided into 32 groups (each group containing 1 ADC)
    The ADC cycle is at 30kHz * 13 = 360 kHz (hence the 13 cycles per AP sample).
    The ADC (from what I understand) goes like this : AP1-AP2-AP3-...-AP11-AP12-LF1-AP1-AP2-...-AP12-LF2-AP1-...
    A. Wyngaard

    For NP2 there are 16 cycles

    The probe always records from all 384 channels; you can disable sites, but they actually still get read back.
    The sample time shifts are always the same for a given channel -- each channel is hardwired to a specific
     ADC and has a specific order in the sampling lineup. So you should always calculate
      the sample shift based on the original channel number. In the SpikeGLX metadata,
      these are listed in the snsSaveChannelSubset field.

    :param version: neuropixel major version 1 or 2
    :param nc: number of channels
    """
    if version == 1:
        adc_channels = 12
        n_cycles = 13
        # version 1 uses 32 ADC that sample 12 channels each
    elif np.floor(version) == 2:
        # version 2 uses 24 ADC that sample 16 channels each
        adc_channels = n_cycles = 16
    adc = np.floor(np.arange(nc) / (adc_channels * 2)) * 2 + np.mod(np.arange(nc), 2)
    sample_shift = np.zeros_like(adc)
    for a in adc:
        sample_shift[adc == a] = np.arange(adc_channels) / n_cycles
    return sample_shift[:nc], adc[:nc]