from os import system
from shutil import move
from platform import architecture
from tempfile import NamedTemporaryFile


cmd = '''rm -rf mojosetup output
sudo apt-get install mercurial cmake libgtk2.0-dev
hg clone http://hg.icculus.org/icculus/mojosetup
cd mojosetup; mkdir cmake-build; cd cmake-build
cmake -DCMAKE_BUILD_TYPE=MinSizeRel -DMOJOSETUP_LUALIB_IO=TRUE \
  -DMOJOSETUP_LUALIB_OS=FALSE -DMOJOSETUP_LUALIB_MATH=FALSE \
  -DMOJOSETUP_LUALIB_DB=FALSE -DMOJOSETUP_LUALIB_PACKAGE=FALSE \
  -DMOJOSETUP_LUALIB_BIT=FALSE -DMOJOSETUP_LUALIB_CORO=FALSE \
  -DMOJOSETUP_GUI_STDIO=FALSE -DMOJOSETUP_GUI_STDIO_STATIC=FALSE \
  -DMOJOSETUP_GUI_NCURSES=FALSE -DMOJOSETUP_ARCHIVE_TAR=FALSE \
  -DMOJOSETUP_ARCHIVE_TAR_GZ=FALSE -DMOJOSETUP_ARCHIVE_TAR_BZ2=FALSE \
  -DMOJOSETUP_ARCHIVE_TAR_XZ=FALSE -DMOJOSETUP_IMAGE_PNG=FALSE \
  -DMOJOSETUP_IMAGE_JPG=FALSE -DMOJOSETUP_URL_HTTP=FALSE \
  -DMOJOSETUP_URL_FTP=FALSE -DMOJOSETUP_BUILD_LUAC=FALSE \
  -DMOJOSETUP_GUI_GTKPLUS2=FALSE -DMOJOSETUP_GUI_GTKPLUS2_STATIC=FALSE \
  -DMOJOSETUP_GUI_STDIO=TRUE -DMOJOSETUP_GUI_STDIO_STATIC=TRUE ..
make; cd ../..; mkdir output; cd output; mkdir data scripts guis meta; cd ..
cp mojosetup/cmake-build/mojosetup output/mojosetup
cp mojosetup/scripts/* output/scripts
# eventually, libs in guis
cp -r mojosetup/meta output
rm -rf mojosetup'''


with NamedTemporaryFile(mode='w+t') as ftmp:
    ftmp.write(cmd)
    ftmp.seek(0)
    system('sh ' + ftmp.name)
    suff = {'32': '', '64': '_64'}
    fdst = 'output/mojosetupx86' + suff[architecture()[0][:2]]
    move('output/mojosetup', fdst)
