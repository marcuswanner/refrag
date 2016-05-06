refrag
======

A memory management visualizer. For CS 3114 at Virginia Tech, the final project involved creating a memory manager which essentially works like a primitive malloc(). While debugging my implementation, I found it helpful to visualize logs of reads, writes, and frees. I wrote a python script that uses curses to display an animated, colorized, and annotated representation of memory during the execution of the memory manager under test.

## Screenshots

![](doc/screenshot-short.png)

![](doc/screenshot-med.png)

![](doc/screenshot-long.png)

## Usage

```
git clone https://github.com/marcuswanner/refrag.git
cd refrag
python3 refrag.py writes-med.txt
```
