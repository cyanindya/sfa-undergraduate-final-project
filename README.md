# Git repository for Sinantya F. Anindya's undergraduate program final project (2016)
### Description
This repository contains the codes used in undergraduate final project "Prototype of EEG-based Home Appliances Control System" *("Prototipe Sistem Kendali Peralatan Rumah Berbasis Elektroensefalogram")* by Sinantya F. Anindya, which was conducted in February-June 2016 in Department of Electrical Engineering, Institut Teknologi Nasional, Bandung. The codes are written in Python.

### Usage
The requirements to run the codes are as follows:
* Python 3.5
* PyQt4 (for Spyder)
* SciPy (NumPy, SciPy, IPython, Matplotlib, and Scikit-Learn)
* Spyder

### Testing Environment
The codes are last tested with Anaconda 2.5.0 and following package versions:
* Python 3.5.1
* SciPy 0.17.0
* Spyder 2.3.8
* NumPy 1.10.4
* IPython 4.0.3
* Matplotlib 1.5.1
* Scikit-Learn 0.17.1
* PyQt 4.11.4
It should be noted that some files (e.g. classifier pickle files) may be incompatible with different version of the packages, and as such, they may need to be re-compiled.

The datasets used for prototyping the system belong to Bakardjian et al. (2010) (http://www.bakardjian.com/work/ssvep_data_Bakardjian.html) and AVI SSVEP Dataset (http://www.setzner.com). As for the testing data collected using OpenBCI V3, they can be found within this repository.

### Permission and License
The codes provided within this repository is **intended for non-commercial and academic purposes only**. This is due to the prohibition to use the reference datasets for commercial purposes without the original owners' permission. If you wish to use the codes commercial usage, please contact the respective owners of the reference datasets first.

If any portion of the codes is used within research, kindly please cite the report of this final project.

### Reference
Bakardjian H, Tanaka T, Cichocki A, Optimization of SSVEP brain responses with application to eight-command Brain–Computer Interface, *Neurosci Lett*, 2010, 469(1):34-38. (http://dx.doi.org/10.1016/j.neulet.2009.11.039)
