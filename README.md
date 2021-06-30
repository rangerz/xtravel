# xtravel

The hotel 🏨 and campsite 🏕️  availability checker for **X**anterra **Travel** Collection (https://www.xanterra.com/)



### Suppport Locations

- [Grand Canyon National Park](https://secure.grandcanyonlodges.com/booking/lodging) (GCNP)
- [Glacier National Park Lodges](https://secure.glaciernationalparklodges.com/booking/lodging) (GNP)
- [The Grand Hotel](https://secure.grandcanyongrandhotel.com/booking/lodging) (GCGH)
- [Yellowstone National Park](https://secure.yellowstonenationalparklodges.com/booking/lodging) (YSNP)
- [Zion National Park](https://secure.zionlodge.com/booking/lodging) (UTZN)



### Install

```bash
# Setup virtualenv (Recommend)
virtualenv venv -p python3
source venv/bin/activate

pip install -r requirements.txt
```



### Usage

#### Help Message

```bash
$ python xtravel.py --help
usage: xtravel.py [-h] [--area AREA] [--start-date START_DATE] [--end-date END_DATE] [--adults ADULTS]
                  [--children CHILDREN]

optional arguments:
  -h, --help            show this help message and exit
  --area AREA           grandcanyonlodges, glaciernationalparklodges, grandcanyongrandhotel,
                        yellowstonenationalparklodges, zionlodge
  --start-date START_DATE
                        Start Date (MM/DD/YYYY)
  --end-date END_DATE   End Date (MM/DD/YYYY)
  --adults ADULTS       Number of Adults (1~8)
  --children CHILDREN   Number of Children (0~7)
```

#### Use Wizard

```bash
$ python xtravel.py
Area:
> Grand Canyon National Park
  Glacier National Park Lodges
  The Grand Hotel
  Yellowstone National Park
  Zion National Park

Enter start date [08/01/2021]:
Enter end date [08/07/2021]:
Enter number of adults (1~8)[1]: 2
Enter number of children (0~7)[0]:
```

#### Use Parameters

```bash
$ python xtravel.py \
	--area grandcanyonlodges \
	--start-date 08/01/2021 \
	--end-date 08/07/2021 \
	--adults 2 \
	--children 0
```

#### Example Output

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Found the available date !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

| Code   | Hotel Title                            |
|--------|----------------------------------------|
| GLCC   | Cedar Creek Lodge (Columbia Falls, MT) |
| GLLM   | Lake McDonald                          |
| GLMG   | Many Glacier Hotel                     |
| GLRS   | Rising Sun Motor Inn & Cabins          |
| GLSC   | Swiftcurrent Motor Inn & Cabins        |
| GLVI   | Village Inn at Apgar                   |

|            | GLCC   | GLLM   | GLMG   | GLRS   | GLSC   | GLVI   |
|------------|--------|--------|--------|--------|--------|--------|
| 08/01/2021 | X      | X      | X      | X      | X      | X      |
| 08/02/2021 | O      | X      | X      | X      | X      | X      |
| 08/03/2021 | X      | X      | X      | X      | X      | X      |
| 08/04/2021 | X      | X      | X      | X      | X      | X      |
| 08/05/2021 | X      | X      | X      | X      | X      | X      |
| 08/06/2021 | X      | X      | X      | X      | X      | X      |
| 08/07/2021 | X      | X      | X      | X      | X      | X      |


List:
[08/02/2021] Cedar Creek Lodge (Columbia Falls, MT)

Flexible Date URL: https://secure.glaciernationalparklodges.com/booking/lodging-flex-search?dateFrom=08-01-2021&adults=4&children=0&nights=6&destination=ALL
```



### TODO

- Infinite loop check with delay time
- Notification (Pushbullet API)
- Random User Agent
- Select location parameter
- Make order with login user by selenium
- Dockerfile (Github workflow)



### License

[MIT](https://opensource.org/licenses/MIT)

