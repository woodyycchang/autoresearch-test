# R629 step 01

**Timestamp:** 2026-05-19T19:13:42Z

## Scan focus
Random matrix theory (RMT), specifically the Marchenko-Pastur distribution, as a mechanism source for weight-spectrum allocation. MP gives the exact distribution of eigenvalues of XX^T/N when X has i.i.d. entries; this distribution literally describes randomly-initialized neural weight matrices. The candidate: detect deviation of weight singular-value distribution from MP envelope as a "structural-information" signal; allocate fine-tuning capacity to layers with high deviation.

## Motivation
mechanism_transfer: MP distribution IS the eigenvalue law of large random matrices. Bouchaud-Potters cleaning literally uses MP to denoise estimated covariance matrices. The candidate transfers MP eigenvalue-cleaning to per-layer weight spectra.
