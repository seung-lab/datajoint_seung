# Pinky (Public)

### Tables
- Scan: Scan information of functional scans Baylor recorded. Total of 9 scans exist.
    - `scan_id`: Scan id ([1,2,3,4,5,6,7,8,9]).
    - `depth`: z index in the 2p structural stack (0 ~ 330).
    - `laser_power`: Laser power.
    - `wavelength`: Wavelength.
    
- Slice: Slice information of functional scans. 3 slices exist for each scan.
    - `scan_id`: Scan id of the slice.
    - `slice_idx`: Slice index within each scan ([1,2,3]).
    - `depth`: z index in the 2p structural stack (0 ~ 330).
    
- Stimulus: Visual stimulus used for the functional recording. The slices in each scan are recorded simultaneously.
    - `scan_id`: Scan id.
    - `movie`: Visual stimulus (90 x 160 x 27100 array). Time resolution is 14.83 frame/s. 
    - `condition`: Angle of the visual stimulus (length 27100 vector). Angles range between 0&deg; and 360&deg; with resolution of 22.5&deg;. The directions of the stimulus is pseudorandomly-ordered.
    
- Neuron: Cells with cell body.
    - `segment_id`: Segment id in materialization `v185`.
    - `manual_id`: Id of manual masks.
    
- Soma: Soma information.
    - `soma_x`: Soma x-axis location [nm]
    - `soma_y`: Soma y-axis location [nm]
    - `soma_z`: Soma z-axis location [nm]
  
- EASETrace: Trace from EASE mask.
    - `trace_raw`: Raw traces.
    - `trace`: Denoised and detrended traces.
    - `spike`: Deconvoluted traces using Vogelstein et al., 2009

- EASETuning: Tuning curve computed from EASE trace.
    - `tune_curve`: Direction tuning curve (16 directions).
    - `osi`: Orientation selectivity index.
    - `osi_p`: p-value for orientation selectivity (significantly tuned if p<0.01).
    - `dsi`: Direction selectivity index.
    - `dsi_p`: p-value for direction selectivity (significantly tuned if p<0.01).   
