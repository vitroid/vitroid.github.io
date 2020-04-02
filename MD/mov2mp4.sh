base=`basename $1`
ffmpeg -i $1 -pix_fmt yuv420p ../img/$base.mp4
ffmpeg -i $1 -vframes 1 ../img/$base.png

