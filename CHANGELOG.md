# h.265 Encoder Script
### VERSION 1.0.1


## Unreleased


## Version 1.0.1
 ### Added
  - Logic to prevent thread counts in `config.ini` exceeding actual CPU thread counts and throwing errors.
  - Examples in `config.ini` for popular codec options.

 ### Removed
  - Generic module imports over specified functions, per Python recommended practices.

 ### Changed
  - Character length and variable/function names to comply with PEP 8