# -*- coding: utf-8 -*-



class HmacMd5 (object):
    """
    A HMAC-MD5 implementation that is compatible with the Standford's
    PwdHash implementation in Javascript, both for ASCII and Unicode.
    Python's built-in HMAC-MD5 implementation only supports ASCII.-
    """
    @staticmethod
    def _wrap_signed_int32 (integer):
        """
        Converts 'integer' to a valid signed 32-bit integer.-
        """
        if integer > 2**31:
            integer = (0xFFFFFFFF - integer + 1) * -1
        return integer

    @staticmethod
    def _safe_add (x, y):
        """
        Add integers, wrapping at 2^32.
        This uses 16-bit operations internally.-
        """
        lsw = (x & 0xFFFF) + (y & 0xFFFF)
        msw = (x >> 16) + (y >> 16) + (lsw >> 16)
        #
        # msw should be a valid 32-bit signed integer
        #
        msw = HmacMd5._wrap_signed_int32 (msw << 16)
        return msw | (lsw & 0xFFFF)

    @staticmethod
    def _bit_rol (num, cnt):
        """
        Implements the Javascript bitwise rotation of a
        32-bit number.-
        """
        #
        # take only the lower 32 bits into account
        # when left shifting
        #
        lwr_32 = (num << cnt) & 0xFFFFFFFF
        #
        # implement Javascript's zero-filling right shift (>>>)
        #
        if num < 0:
            num = 0xFFFFFFFF + num + 1
        ret_val  = num >> (32 - cnt)
        ret_val |= lwr_32
        #
        # ret_val should be a 32-bit signed number
        #
        ret_val = HmacMd5._wrap_signed_int32 (ret_val)
        return ret_val

    #
    # these functions implement the four basic operations the algorithm uses
    #
    @staticmethod
    def _md5_cmn (q, a, b, x, s, t):
        return HmacMd5._safe_add (HmacMd5._bit_rol (HmacMd5._safe_add (
               HmacMd5._safe_add (a, q), HmacMd5._safe_add (x, t)), s), b)

    @staticmethod
    def _md5_ff (a, b, c, d, x, s, t):
        return HmacMd5._md5_cmn ((b & c) | ((~b) & d), a, b, x, s, t)

    @staticmethod
    def _md5_gg (a, b, c, d, x, s, t):
        return HmacMd5._md5_cmn ((b & d) | (c & (~d)), a, b, x, s, t)

    @staticmethod
    def _md5_hh (a, b, c, d, x, s, t):
        return HmacMd5._md5_cmn (b ^ c ^ d, a, b, x, s, t)

    @staticmethod
    def _md5_ii (a, b, c, d, x, s, t):
        return HmacMd5._md5_cmn (c ^ (b | (~d)), a, b, x, s, t)


    @staticmethod
    def core_md5 (lst, bit_count):
        """
        Calculates the MD5 of list 'lst' containing little-endian words
        and a bit lenght of 'bit_count'.-
        """
        #
        # append padding
        #
        idx = bit_count >> 5
        for i in range (idx - len (lst) + 1):
            lst.append (0)
        lst[idx] |= 0x80 << (bit_count % 32)

        idx = (((bit_count + 64) >> 9) << 4) + 14
        for i in range (idx - len (lst) + 2):
            lst.append (0)
        lst[idx] = bit_count

        a =  1732584193
        b = -271733879
        c = -1732584194
        d =  271733878

        for i in range (0, len (lst) - 1, 16):
            old_a = a
            old_b = b
            old_c = c
            old_d = d

            a = HmacMd5._md5_ff (a, b, c, d, lst[i+ 0], 7 , -680876936)
            d = HmacMd5._md5_ff (d, a, b, c, lst[i+ 1], 12, -389564586)
            c = HmacMd5._md5_ff (c, d, a, b, lst[i+ 2], 17,  606105819)
            b = HmacMd5._md5_ff (b, c, d, a, lst[i+ 3], 22, -1044525330)
            a = HmacMd5._md5_ff (a, b, c, d, lst[i+ 4], 7 , -176418897)
            d = HmacMd5._md5_ff (d, a, b, c, lst[i+ 5], 12,  1200080426)
            c = HmacMd5._md5_ff (c, d, a, b, lst[i+ 6], 17, -1473231341)
            b = HmacMd5._md5_ff (b, c, d, a, lst[i+ 7], 22, -45705983)
            a = HmacMd5._md5_ff (a, b, c, d, lst[i+ 8], 7 ,  1770035416)
            d = HmacMd5._md5_ff (d, a, b, c, lst[i+ 9], 12, -1958414417)
            c = HmacMd5._md5_ff (c, d, a, b, lst[i+10], 17, -42063)
            b = HmacMd5._md5_ff (b, c, d, a, lst[i+11], 22, -1990404162)
            a = HmacMd5._md5_ff (a, b, c, d, lst[i+12], 7 ,  1804603682)
            d = HmacMd5._md5_ff (d, a, b, c, lst[i+13], 12, -40341101)
            c = HmacMd5._md5_ff (c, d, a, b, lst[i+14], 17, -1502002290)
            b = HmacMd5._md5_ff (b, c, d, a, lst[i+15], 22,  1236535329)

            a = HmacMd5._md5_gg (a, b, c, d, lst[i+ 1], 5 , -165796510)
            d = HmacMd5._md5_gg (d, a, b, c, lst[i+ 6], 9 , -1069501632)
            c = HmacMd5._md5_gg (c, d, a, b, lst[i+11], 14,  643717713)
            b = HmacMd5._md5_gg (b, c, d, a, lst[i+ 0], 20, -373897302)
            a = HmacMd5._md5_gg (a, b, c, d, lst[i+ 5], 5 , -701558691)
            d = HmacMd5._md5_gg (d, a, b, c, lst[i+10], 9 ,  38016083)
            c = HmacMd5._md5_gg (c, d, a, b, lst[i+15], 14, -660478335)
            b = HmacMd5._md5_gg (b, c, d, a, lst[i+ 4], 20, -405537848)
            a = HmacMd5._md5_gg (a, b, c, d, lst[i+ 9], 5 ,  568446438)
            d = HmacMd5._md5_gg (d, a, b, c, lst[i+14], 9 , -1019803690)
            c = HmacMd5._md5_gg (c, d, a, b, lst[i+ 3], 14, -187363961)
            b = HmacMd5._md5_gg (b, c, d, a, lst[i+ 8], 20,  1163531501)
            a = HmacMd5._md5_gg (a, b, c, d, lst[i+13], 5 , -1444681467)
            d = HmacMd5._md5_gg (d, a, b, c, lst[i+ 2], 9 , -51403784)
            c = HmacMd5._md5_gg (c, d, a, b, lst[i+ 7], 14,  1735328473)
            b = HmacMd5._md5_gg (b, c, d, a, lst[i+12], 20, -1926607734)

            a = HmacMd5._md5_hh (a, b, c, d, lst[i+ 5], 4 , -378558)
            d = HmacMd5._md5_hh (d, a, b, c, lst[i+ 8], 11, -2022574463)
            c = HmacMd5._md5_hh (c, d, a, b, lst[i+11], 16,  1839030562)
            b = HmacMd5._md5_hh (b, c, d, a, lst[i+14], 23, -35309556)
            a = HmacMd5._md5_hh (a, b, c, d, lst[i+ 1], 4 , -1530992060)
            d = HmacMd5._md5_hh (d, a, b, c, lst[i+ 4], 11,  1272893353)
            c = HmacMd5._md5_hh (c, d, a, b, lst[i+ 7], 16, -155497632)
            b = HmacMd5._md5_hh (b, c, d, a, lst[i+10], 23, -1094730640)
            a = HmacMd5._md5_hh (a, b, c, d, lst[i+13], 4 ,  681279174)
            d = HmacMd5._md5_hh (d, a, b, c, lst[i+ 0], 11, -358537222)
            c = HmacMd5._md5_hh (c, d, a, b, lst[i+ 3], 16, -722521979)
            b = HmacMd5._md5_hh (b, c, d, a, lst[i+ 6], 23,  76029189)
            a = HmacMd5._md5_hh (a, b, c, d, lst[i+ 9], 4 , -640364487)
            d = HmacMd5._md5_hh (d, a, b, c, lst[i+12], 11, -421815835)
            c = HmacMd5._md5_hh (c, d, a, b, lst[i+15], 16,  530742520)
            b = HmacMd5._md5_hh (b, c, d, a, lst[i+ 2], 23, -995338651)

            a = HmacMd5._md5_ii (a, b, c, d, lst[i+ 0], 6 , -198630844)
            d = HmacMd5._md5_ii (d, a, b, c, lst[i+ 7], 10,  1126891415)
            c = HmacMd5._md5_ii (c, d, a, b, lst[i+14], 15, -1416354905)
            b = HmacMd5._md5_ii (b, c, d, a, lst[i+ 5], 21, -57434055)
            a = HmacMd5._md5_ii (a, b, c, d, lst[i+12], 6 ,  1700485571)
            d = HmacMd5._md5_ii (d, a, b, c, lst[i+ 3], 10, -1894986606)
            c = HmacMd5._md5_ii (c, d, a, b, lst[i+10], 15, -1051523)
            b = HmacMd5._md5_ii (b, c, d, a, lst[i+ 1], 21, -2054922799)
            a = HmacMd5._md5_ii (a, b, c, d, lst[i+ 8], 6 ,  1873313359)
            d = HmacMd5._md5_ii (d, a, b, c, lst[i+15], 10, -30611744)
            c = HmacMd5._md5_ii (c, d, a, b, lst[i+ 6], 15, -1560198380)
            b = HmacMd5._md5_ii (b, c, d, a, lst[i+13], 21,  1309151649)
            a = HmacMd5._md5_ii (a, b, c, d, lst[i+ 4], 6 , -145523070)
            d = HmacMd5._md5_ii (d, a, b, c, lst[i+11], 10, -1120210379)
            c = HmacMd5._md5_ii (c, d, a, b, lst[i+ 2], 15,  718787259)
            b = HmacMd5._md5_ii (b, c, d, a, lst[i+ 9], 21, -343485551)

            a = HmacMd5._safe_add (a, old_a)
            b = HmacMd5._safe_add (b, old_b)
            c = HmacMd5._safe_add (c, old_c)
            d = HmacMd5._safe_add (d, old_d)

        return [a, b, c, d]


    @staticmethod
    def str2binl (string, chrsz):
        """
        Converts 'string' to a list of little-endian words.
        If 'chrsz' is 8 (ASCII), characters >255 have their hi-byte
        silently ignored:

        string  the string to convert;
        chrsz   number of bits per input character.-
        """
        binl  = [0]
        mask = (1 << chrsz) - 1

        for i in range (0, len(string) * chrsz, chrsz):
            tmp = ord (string[i / chrsz]) & mask
            tmp = tmp << (i % 32)
            idx = i >> 5
            if idx == len(binl):
                binl.append (0)
            binl[idx] |= tmp

        return binl


    @staticmethod
    def core_hmac_md5 (key, data):
        """
        Calculates the HMAC-MD5, of a key and some data.-
        """
        #
        # bits per input character: 8 - ASCII; 16 - Unicode
        #
        chrsz = 8

        bkey = HmacMd5.str2binl (key, chrsz)
        if len(bkey) > 16:
            bkey = HmacMd5.core_md5 (bkey,
                                     len(key) * chrsz)

        ipad = [0] * 16
        opad = [0] * 16
        for i in range (len(bkey)):
            ipad[i] = bkey[i] ^ 0x36363636
            opad[i] = bkey[i] ^ 0x5C5C5C5C

        for i in range (len(bkey), len(ipad)):
            ipad[i] = 0x36363636
            opad[i] = 0x5C5C5C5C

        ipad += HmacMd5.str2binl (data, chrsz)
        my_hash = HmacMd5.core_md5 (ipad,
                                    512 + len(data) * chrsz)
        opad += my_hash

        return HmacMd5.core_md5 (opad,
                                 512 + 128)

