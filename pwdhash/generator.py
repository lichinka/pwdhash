import re
import itertools



class PwdHashGenerator (object):
    """
    Implements Stanford's PwdHash theft-resistant password generation.-
    """
    @staticmethod
    def _apply_constraints (phash, size, nonalphanumeric):
        """
        Fiddle with the password a bit after hashing it so that it will
        get through most website filters. We require one upper and lower
        case, one digit, and we look at the user's password to determine
        if there should be at least one non-alphanumeric or not.-
        """
        starting_size = size - 4
        result = phash[:starting_size]

        extras = itertools.chain((ord(ch) for ch in phash[starting_size:]),
                                 itertools.repeat(0))
        extra_chars = (chr(ch) for ch in extras)
        nonword = re.compile(r'\W')

        def next_between(start, end):
            interval = ord(end) - ord(start) + 1
            offset = extras.next() % interval
            return chr(ord(start) + offset)

        for elt, repl in (
            (re.compile('[A-Z]'), lambda: next_between('A', 'Z')),
            (re.compile('[a-z]'), lambda: next_between('a', 'z')),
            (re.compile('[0-9]'), lambda: next_between('0', '9'))):
            if len(elt.findall(result)) != 0:
                result += extra_chars.next()
            else:
                result += repl()

        if len(nonword.findall(result)) != 0 and nonalphanumeric:
            result += extra_chars.next()
        else:
            result += '+'

        while len(nonword.findall(result)) != 0 and not nonalphanumeric:
            result = nonword.sub(next_between('A', 'Z'), result, 1)

        amount = extras.next() % len(result)
        result = result[amount:] + result[0:amount]

        return result


    @staticmethod
    def _reversible_hash (num):
        """
        Applies a reversible hash function to the 32-bit number 'num'.-
        """
        return ((0x0000FFFF & num)<<16) + ((0xFFFF0000 & num)>>16)

    """
    def _b64_hmac_md5 (key, data):
        ""
        Returns a base64-encoded HMAC-MD5 for key and data, with the
        trailing '=' stripped.-
        ""
        import unicodedata

        #
        # the HMAC object does not support Unicode data, so we have
        # to normalize the string before hashing it
        #
        norm_key = unicodedata.normalize ('NFKD', key)
        norm_key = norm_key.encode ('ascii', 'ignore')

        bdigest = hmac.HMAC (norm_key, data).digest ( )
        bdigest = bdigest.encode ('base64').strip ( )

        return re.sub ('=+$', '', bdigest)
    """


    def _extract_domain (self, uri):
        """
        Returns the domain name from 'uri'.-
        """
        uri = re.sub ('https?://', '', uri)
        uri = re.match ('([^/]+)', uri).groups()[0]
        domain = '.'.join (uri.split('.')[-2:])
        if domain in self.domains:
            domain = '.'.join (uri.split ('.')[-3:])
        return domain


    def __init__ (self, master_pwd):
        """
        Instantiates a new object with the received 'master_pwd',
        a.k.a. the key for generating passwords.-
        """
        #
        # the password prefix used to activate the browser plugin
        #
        self.password_prefix = '@@'

        #
        # make sure the user did not make the mistake of including the
        # prefix for activating the browser plugin
        #
        if master_pwd.startswith (self.password_prefix):
            master_pwd = master_pwd[len (self.password_prefix):]

        #
        # save the master password with a reversible hash function,
        # for better security and to stay compatible with PwdHash
        #
        self.hashed_pwd = [self._reversible_hash (ord (c)) for c in master_pwd]
        del master_pwd

        #
        # set of domain suffixes to be kept
        #
        self.domains = ["ab.ca", "ac.ac", "ac.at", "ac.be", "ac.cn", "ac.il",
                    "ac.in", "ac.jp", "ac.kr", "ac.nz", "ac.th", "ac.uk",
                    "ac.za", "adm.br", "adv.br", "agro.pl", "ah.cn", "aid.pl",
                    "alt.za", "am.br", "arq.br", "art.br", "arts.ro",
                    "asn.au", "asso.fr", "asso.mc", "atm.pl", "auto.pl",
                    "bbs.tr", "bc.ca", "bio.br", "biz.pl", "bj.cn", "br.com",
                    "cn.com", "cng.br", "cnt.br", "co.ac", "co.at", "co.il",
                    "co.in", "co.jp", "co.kr", "co.nz", "co.th", "co.uk",
                    "co.za", "com.au", "com.br", "com.cn", "com.ec", "com.fr",
                    "com.hk", "com.mm", "com.mx", "com.pl", "com.ro",
                    "com.ru", "com.sg", "com.tr", "com.tw", "cq.cn", "cri.nz",
                    "de.com", "ecn.br", "edu.au", "edu.cn", "edu.hk",
                    "edu.mm", "edu.mx", "edu.pl", "edu.tr", "edu.za",
                    "eng.br", "ernet.in", "esp.br", "etc.br", "eti.br",
                    "eu.com", "eu.lv", "fin.ec", "firm.ro", "fm.br", "fot.br",
                    "fst.br", "g12.br", "gb.com", "gb.net", "gd.cn", "gen.nz",
                    "gmina.pl", "go.jp", "go.kr", "go.th", "gob.mx", "gov.br",
                    "gov.cn", "gov.ec", "gov.il", "gov.in", "gov.mm",
                    "gov.mx", "gov.sg", "gov.tr", "gov.za", "govt.nz",
                    "gs.cn", "gsm.pl", "gv.ac", "gv.at", "gx.cn", "gz.cn",
                    "hb.cn", "he.cn", "hi.cn", "hk.cn", "hl.cn", "hn.cn",
                    "hu.com", "idv.tw", "ind.br", "inf.br", "info.pl",
                    "info.ro", "iwi.nz", "jl.cn", "jor.br", "jpn.com",
                    "js.cn", "k12.il", "k12.tr", "lel.br", "ln.cn", "ltd.uk",
                    "mail.pl", "maori.nz", "mb.ca", "me.uk", "med.br",
                    "med.ec", "media.pl", "mi.th", "miasta.pl", "mil.br",
                    "mil.ec", "mil.nz", "mil.pl", "mil.tr", "mil.za", "mo.cn",
                    "muni.il", "nb.ca", "ne.jp", "ne.kr", "net.au", "net.br",
                    "net.cn", "net.ec", "net.hk", "net.il", "net.in",
                    "net.mm", "net.mx", "net.nz", "net.pl", "net.ru",
                    "net.sg", "net.th", "net.tr", "net.tw", "net.za", "nf.ca",
                    "ngo.za", "nm.cn", "nm.kr", "no.com", "nom.br", "nom.pl",
                    "nom.ro", "nom.za", "ns.ca", "nt.ca", "nt.ro", "ntr.br",
                    "nx.cn", "odo.br", "on.ca", "or.ac", "or.at", "or.jp",
                    "or.kr", "or.th", "org.au", "org.br", "org.cn", "org.ec",
                    "org.hk", "org.il", "org.mm", "org.mx", "org.nz",
                    "org.pl", "org.ro", "org.ru", "org.sg", "org.tr",
                    "org.tw", "org.uk", "org.za", "pc.pl", "pe.ca", "plc.uk",
                    "ppg.br", "presse.fr", "priv.pl", "pro.br", "psc.br",
                    "psi.br", "qc.ca", "qc.com", "qh.cn", "re.kr",
                    "realestate.pl", "rec.br", "rec.ro", "rel.pl", "res.in",
                    "ru.com", "sa.com", "sc.cn", "school.nz", "school.za",
                    "se.com", "se.net", "sh.cn", "shop.pl", "sk.ca",
                    "sklep.pl", "slg.br", "sn.cn", "sos.pl", "store.ro",
                    "targi.pl", "tj.cn", "tm.fr", "tm.mc", "tm.pl", "tm.ro",
                    "tm.za", "tmp.br", "tourism.pl", "travel.pl", "tur.br",
                    "turystyka.pl", "tv.br", "tw.cn", "uk.co", "uk.com",
                    "uk.net", "us.com", "uy.com", "vet.br", "web.za",
                    "web.com", "www.ro", "xj.cn", "xz.cn", "yk.ca", "yn.cn",
                    "za.com"]


    def generate (self, uri):
        """
        Returns a newly-generated PwdHash password for the received 'uri'.-
        """
        from pwdhash.md5 import HmacMd5

        #
        # get the master password of this generator from the hashed list
        #
        passwd = [unichr (self._reversible_hash (c)) for c in self.hashed_pwd]
        passwd = ''.join (passwd)
        #
        # extract the domain from the received URI
        #
        realm = self._extract_domain (uri)
        #
        # the lenght of the generated password
        #
        size = len (passwd) + len (self.password_prefix)
        #
        # whether to include non-alphanumeric characters in the
        # generated password
        #
        non_alpha = len (re.findall (r'\W', passwd)) != 0
        #
        # generate the password
        #
        pwd_hash = HmacMd5.b64_hmac_md5 (passwd, realm)
        del passwd

        return self._apply_constraints (pwd_hash, size, non_alpha)

