import struct
import  ctypes


if __name__ == '__main__':
    s = 'string data\0davidsun\0photograph'
    print len(s)
    buf = struct.pack(str(len(s))+'s',  s)

    print "buf:", buf

    idx = 0
    s1,s2,s3 = struct.unpack('s'+'\0'+'s'+'\0'+'s', buf[:])
    print "l:", s1,s2,s3

