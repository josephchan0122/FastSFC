import traceback
import botocore
import boto3
import urllib.request
import urllib.error
import urllib.parse
import os
import json
from django.conf import settings


""" Mapping of extension to AWS S3 content type """
filetypes = {
    "3gp": "video/3gpp",
    "3gp2": "video/3gpp2",
    "3gpp": "video/3gpp",
    "aa": "audio/audible",
    "aac": "audio/vnd.dlna.adts",
    "aax": "audio/vnd.audible.aax",
    "addin": "text/xml",
    "adt": "audio/vnd.dlna.adts",
    "adts": "audio/vnd.dlna.adts",
    "ai": "application/postscript",
    "aif": "audio/aiff",
    "aifc": "audio/aiff",
    "aiff": "audio/aiff",
    "application": "application/x-ms-application",
    "asax": "application/xml",
    "ascx": "application/xml",
    "asf": "video/x-ms-asf",
    "ashx": "application/xml",
    "asmx": "application/xml",
    "aspx": "application/xml",
    "asx": "video/x-ms-asf",
    "au": "audio/basic",
    "avi": "video/avi",
    "bmp": "image/bmp",
    "btapp": "application/x-bittorrent-app",
    "btinstall": "application/x-bittorrent-appinst",
    "btkey": "application/x-bittorrent-key",
    "btsearch": "application/x-bittorrentsearchdescription+xml",
    "btskin": "application/x-bittorrent-skin",
    "cat": "application/vnd.ms-pki.seccat",
    "cd": "text/plain",
    "cer": "application/x-x509-ca-cert",
    "config": "application/xml",
    "contact": "text/x-ms-contact",
    "crl": "application/pkix-crl",
    "crt": "application/x-x509-ca-cert",
    "cs": "text/plain",
    "csproj": "text/plain",
    "css": "text/css",
    "csv": "application/vnd.ms-excel",
    "datasource": "application/xml",
    "der": "application/x-x509-ca-cert",
    "dib": "image/bmp",
    "dll": "application/x-msdownload",
    "doc": "application/msword",
    "docm": "application/vnd.ms-word.document.macroEnabled.12",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "dot": "application/msword",
    "dotm": "application/vnd.ms-word.template.macroEnabled.12",
    "dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    "dtd": "application/xml-dtd",
    "dtsconfig": "text/xml",
    "eps": "application/postscript",
    "exe": "application/x-msdownload",
    "fdf": "application/vnd.fdf",
    "fif": "application/fractals",
    "gif": "image/gif",
    "group": "text/x-ms-group",
    "hdd": "application/x-virtualbox-hdd",
    "hqx": "application/mac-binhex40",
    "hta": "application/hta",
    "htc": "text/x-component",
    "htm": "text/html",
    "html": "text/html",
    "hxa": "application/xml",
    "hxc": "application/xml",
    "hxd": "application/octet-stream",
    "hxe": "application/xml",
    "hxf": "application/xml",
    "hxh": "application/octet-stream",
    "hxi": "application/octet-stream",
    "hxk": "application/xml",
    "hxq": "application/octet-stream",
    "hxr": "application/octet-stream",
    "hxs": "application/octet-stream",
    "hxt": "application/xml",
    "hxv": "application/xml",
    "hxw": "application/octet-stream",
    "ico": "image/x-icon",
    "ics": "text/calendar",
    "ipa": "application/x-itunes-ipa",
    "ipg": "application/x-itunes-ipg",
    "ipsw": "application/x-itunes-ipsw",
    "iqy": "text/x-ms-iqy",
    "iss": "text/plain",
    "ite": "application/x-itunes-ite",
    "itlp": "application/x-itunes-itlp",
    "itls": "application/x-itunes-itls",
    "itms": "application/x-itunes-itms",
    "itpc": "application/x-itunes-itpc",
    "jfif": "image/jpeg",
    "jnlp": "application/x-java-jnlp-file",
    "jpe": "image/jpeg",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "js": "application/javascript",
    "latex": "application/x-latex",
    "library-ms": "application/windows-library+xml",
    "m1v": "video/mpeg",
    "m2t": "video/vnd.dlna.mpeg-tts",
    "m2ts": "video/vnd.dlna.mpeg-tts",
    "m2v": "video/mpeg",
    "m3u": "audio/mpegurl",
    "m3u8": "audio/x-mpegurl",
    "m4a": "audio/m4a",
    "m4b": "audio/m4b",
    "m4p": "audio/m4p",
    "m4r": "audio/x-m4r",
    "m4v": "video/x-m4v",
    "magnet": "application/x-magnet",
    "man": "application/x-troff-man",
    "master": "application/xml",
    "mht": "message/rfc822",
    "mhtml": "message/rfc822",
    "mid": "audio/mid",
    "midi": "audio/mid",
    "mod": "video/mpeg",
    "mov": "video/quicktime",
    "mp2": "audio/mpeg",
    "mp2v": "video/mpeg",
    "mp3": "audio/mpeg",
    "mp4": "video/mp4",
    "mp4v": "video/mp4",
    "mpa": "video/mpeg",
    "mpe": "video/mpeg",
    "mpeg": "video/mpeg",
    "mpf": "application/vnd.ms-mediapackage",
    "mpg": "video/mpeg",
    "mpv2": "video/mpeg",
    "mts": "video/vnd.dlna.mpeg-tts",
    "odc": "text/x-ms-odc",
    "odg": "application/vnd.oasis.opendocument.graphics",
    "odm": "application/vnd.oasis.opendocument.text-master",
    "odp": "application/vnd.oasis.opendocument.presentation",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "odt": "application/vnd.oasis.opendocument.text",
    "otg": "application/vnd.oasis.opendocument.graphics-template",
    "oth": "application/vnd.oasis.opendocument.text-web",
    "ots": "application/vnd.oasis.opendocument.spreadsheet-template",
    "ott": "application/vnd.oasis.opendocument.text-template",
    "ova": "application/x-virtualbox-ova",
    "ovf": "application/x-virtualbox-ovf",
    "oxt": "application/vnd.openofficeorg.extension",
    "p10": "application/pkcs10",
    "p12": "application/x-pkcs12",
    "p7b": "application/x-pkcs7-certificates",
    "p7c": "application/pkcs7-mime",
    "p7m": "application/pkcs7-mime",
    "p7r": "application/x-pkcs7-certreqresp",
    "p7s": "application/pkcs7-signature",
    "pcast": "application/x-podcast",
    "pdf": "application/pdf",
    "pdfxml": "application/vnd.adobe.pdfxml",
    "pdx": "application/vnd.adobe.pdx",
    "pfx": "application/x-pkcs12",
    "pko": "application/vnd.ms-pki.pko",
    "pls": "audio/scpls",
    "png": "image/png",
    "pot": "application/vnd.ms-powerpoint",
    "potm": "application/vnd.ms-powerpoint.template.macroEnabled.12",
    "potx": "application/vnd.openxmlformats-officedocument.presentationml.template",
    "ppa": "application/vnd.ms-powerpoint",
    "ppam": "application/vnd.ms-powerpoint.addin.macroEnabled.12",
    "pps": "application/vnd.ms-powerpoint",
    "ppsm": "application/vnd.ms-powerpoint.slideshow.macroEnabled.12",
    "ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
    "ppt": "application/vnd.ms-powerpoint",
    "pptm": "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "prf": "application/pics-rules",
    "ps": "application/postscript",
    "psc1": "application/PowerShell",
    "pwz": "application/vnd.ms-powerpoint",
    "py": "text/plain",
    "pyw": "text/plain",
    "rat": "application/rat-file",
    "rc": "text/plain",
    "rc2": "text/plain",
    "rct": "text/plain",
    "rdlc": "application/xml",
    "resx": "application/xml",
    "rmi": "audio/mid",
    "rmp": "application/vnd.rn-rn_music_package",
    "rqy": "text/x-ms-rqy",
    "rtf": "application/msword",
    "sct": "text/scriptlet",
    "settings": "application/xml",
    "shtml": "text/html",
    "sit": "application/x-stuffit",
    "sitemap": "application/xml",
    "skin": "application/xml",
    "sldm": "application/vnd.ms-powerpoint.slide.macroEnabled.12",
    "sldx": "application/vnd.openxmlformats-officedocument.presentationml.slide",
    "slk": "application/vnd.ms-excel",
    "sln": "text/plain",
    "slupkg-ms": "application/x-ms-license",
    "snd": "audio/basic",
    "snippet": "application/xml",
    "spc": "application/x-pkcs7-certificates",
    "sst": "application/vnd.ms-pki.certstore",
    "stc": "application/vnd.sun.xml.calc.template",
    "std": "application/vnd.sun.xml.draw.template",
    "stl": "application/vnd.ms-pki.stl",
    "stw": "application/vnd.sun.xml.writer.template",
    "svg": "image/svg+xml",
    "sxc": "application/vnd.sun.xml.calc",
    "sxd": "application/vnd.sun.xml.draw",
    "sxg": "application/vnd.sun.xml.writer.global",
    "sxw": "application/vnd.sun.xml.writer",
    "tga": "image/targa",
    "thmx": "application/vnd.ms-officetheme",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "torrent": "application/x-bittorrent",
    "ts": "video/vnd.dlna.mpeg-tts",
    "tts": "video/vnd.dlna.mpeg-tts",
    "txt": "text/plain",
    "user": "text/plain",
    "vb": "text/plain",
    "vbox": "application/x-virtualbox-vbox",
    "vbox-extpack": "application/x-virtualbox-vbox-extpack",
    "vbproj": "text/plain",
    "vcf": "text/x-vcard",
    "vdi": "application/x-virtualbox-vdi",
    "vdp": "text/plain",
    "vdproj": "text/plain",
    "vhd": "application/x-virtualbox-vhd",
    "vmdk": "application/x-virtualbox-vmdk",
    "vor": "application/vnd.stardivision.writer",
    "vscontent": "application/xml",
    "vsi": "application/ms-vsi",
    "vspolicy": "application/xml",
    "vspolicydef": "application/xml",
    "vspscc": "text/plain",
    "vsscc": "text/plain",
    "vssettings": "text/xml",
    "vssscc": "text/plain",
    "vstemplate": "text/xml",
    "vsto": "application/x-ms-vsto",
    "wal": "interface/x-winamp3-skin",
    "wav": "audio/wav",
    "wave": "audio/wav",
    "wax": "audio/x-ms-wax",
    "wbk": "application/msword",
    "wdp": "image/vnd.ms-photo",
    "website": "application/x-mswebsite",
    "wiz": "application/msword",
    "wlz": "interface/x-winamp-lang",
    "wm": "video/x-ms-wm",
    "wma": "audio/x-ms-wma",
    "wmd": "application/x-ms-wmd",
    "wmv": "video/x-ms-wmv",
    "wmx": "video/x-ms-wmx",
    "wmz": "application/x-ms-wmz",
    "wpl": "application/vnd.ms-wpl",
    "wsc": "text/scriptlet",
    "wsdl": "application/xml",
    "wsz": "interface/x-winamp-skin",
    "wvx": "video/x-ms-wvx",
    "xaml": "application/xaml+xml",
    "xbap": "application/x-ms-xbap",
    "xdp": "application/vnd.adobe.xdp+xml",
    "xdr": "application/xml",
    "xfdf": "application/vnd.adobe.xfdf",
    "xht": "application/xhtml+xml",
    "xhtml": "application/xhtml+xml",
    "xla": "application/vnd.ms-excel",
    "xlam": "application/vnd.ms-excel.addin.macroEnabled.12",
    "xld": "application/vnd.ms-excel",
    "xlk": "application/vnd.ms-excel",
    "xll": "application/vnd.ms-excel",
    "xlm": "application/vnd.ms-excel",
    "xls": "application/vnd.ms-excel",
    "xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    "xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xlt": "application/vnd.ms-excel",
    "xltm": "application/vnd.ms-excel.template.macroEnabled.12",
    "xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    "xlw": "application/vnd.ms-excel",
    "xml": "text/xml",
    "xrm-ms": "text/xml",
    "xsc": "application/xml",
    "xsd": "application/xml",
    "xsl": "text/xml",
    "xslt": "application/xml",
    "xss": "application/xml"
}


class S3(object):
    def __init__(self, region='ap-southeast-1'):
        self.region = region
        self.bucket = settings.AWS_S3_BUCKET

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=region
        )

        self.session = session.resource('s3')

    def create_file(self, key, path, filetype=None):
        """
        Creates file in S3 in default bucket given a local path
        """
        try:
            content_type = self.content_type_from_key(key, filetype)

            self.session.Object(self.bucket, key).put(
                ACL='public-read',
                ContentType=content_type,
                Body=open(path, 'rb'),
            )
            url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(self.region, self.bucket, key)
            return url
        except Exception as e:
            import traceback
            traceback.print_exc()

    def create_file_from_url(self, key, url, filetype=None):
        """
        Creates file in S3 in default bucket given a URL
        """
        try:
            file = urllib.request.urlopen(url, timeout=300).read()
            content_type = self.content_type_from_key(key, filetype)
            self.session.Object(self.bucket, key).put(
                ACL='public-read',
                ContentType=content_type,
                Body=file,
            )
            url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(self.region, self.bucket, key)
            return url
        except Exception as e:
            import traceback
            traceback.print_exc()

    def create_file_from_data(self, key, data, filetype=None):
        """
        Creates file in S3 in default bucket given data
        """
        try:
            content_type = self.content_type_from_key(key, filetype)

            self.session.Object(self.bucket, key).put(
                ACL='public-read',
                ContentType=content_type,
                Body=data,
            )
            url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(self.region, self.bucket, key)
            return url
        except Exception as e:
            import traceback
            traceback.print_exc()

    def content_type_from_key(self, key, filetype=None):
        """
        Infers filetype from extension in key
        key: s3 key
        filetype (optional): override extension in key
        """
        if not filetype:
            _, ext = os.path.splitext(key)
            filetype = ext[1:].lower()

        if filetype in filetypes:
            return filetypes[filetype]
        else:
            return 'binary/octet-stream'

    def check_file_exists(self, key):
        try:
            self.session.Object(self.bucket, key).load()
            return True
        except:
            return False

    def url_from_key(self, key):
        return 'https://s3-{}.amazonaws.com/{}/{}'.format(self.region, self.bucket, key)

    def create_bucket(self, name):
        try:
            self.session.create_bucket(
                Bucket=name.lower(),
                CreateBucketConfiguration={
                    'LocationConstraint': self.region,
                }
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                pass
            else:
                print(e.response['Error']['Code'])
        except Exception as e:
            import traceback
            traceback.print_exc()
