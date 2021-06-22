# pyparsedvd

Parse and extract binary data from dvd files

# Installation
```
python -m pip install pyparsedvd
```
or from Github:
```
python -m pip install git+https://github.com/Ichunjo/pyparsedvd.git
```



# Example

```py
from pyparsedvd import load_vts_pgci


with open('DVD/VIDEO_TS/VTS_01_0.IFO', 'rb') as ifo_file:
    vts_pgci = load_vts_pgci(ifo_file)

    print(vts_pgci)

```

# TODO
* Maybe one day add the sectors left

# Credits
* [ChapterTool](https://github.com/tautcony/ChapterTool)
* [DVD Video Information](http://dvd.sourceforge.net/dvdinfo/ifo.html)
  