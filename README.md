# upc2images
Acquires images corresponding to UPC (Universal Product Code) using upcitemdb.com API

## Requirements

- `Python 3.9`
- `requests~=2.22.0`
- `Pillow~=8.1.0`

## Usage

**UPC (Universal Product Code)** - American standard barcode for tracking goods in stores.

This script works on the API of the [upcitemdb.com](https://www.upcitemdb.com/). The "trial" version is used in the script, which means that you can make a request for 100 UPC per day. 

**Steps to run a script**

- Install `requirements.txt` with command `python -m pip install -r requirements.txt`

- Run the script using the command `python main.py`

  

**Manual setting**

- There is a timeout setting in the script `API_COOL_DOWN_TIMEOUT_SECS`. By default, there is a delay of 10 seconds, because the trial is used.
- To change the plan, in the `API_URL_GET` line, change `/trial/` to `/v1/`
- You can also change the minimum allowed image resolution. The default is 600px by 600px. `WIDTH_DIMENSION` and `HEIGHT_DIMENSION` respectively