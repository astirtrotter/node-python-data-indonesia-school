from urllib.request import urlopen
from threading import Thread

import lxml.html as html
import json, os, shutil, time


class Main:
    def __init__(self):
        if ('data' not in os.listdir( os.getcwd() ) ):
            os.mkdir( 'data' )
            os.mkdir('data/schools')
            f = open('data/done.json', 'w')
            f.write('{}')
            f.close()
        #else:
        #    shutil.rmtree('data')
        #    os.mkdir( 'data' )
        #os.mkdir('data/schools')

        self.thread_count = 0
        self.log("Current PID: {} ".format(os.getpid()) )

        f = open('data/done.json', 'r')
        self.DONE = eval( f.read() )
        f.close()
        

        if ('address.txt' in os.listdir(os.getcwd()) ):
            f = open('address.txt' ,'r')
            address = f.read().split('\n')
            f.close()

            for addr in address:
                if (len(addr) < 15 ):
                    continue
                if (addr.endswith('/sp') or addr.endswith('/sp/') ):
                    Thread(target = self.parse_first).start()
                elif ('/sp/1/' in addr):
                    cur_item = {'kode_wilayah': addr.split('/')[-1], 'id_level_wilayah': 1 }
                    URL = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah={}&kode_wilayah={}&semester_id=20191'.format( cur_item['id_level_wilayah'], cur_item['kode_wilayah'].strip().rstrip() )
                    Thread(target = self.parse_second, args = (URL, cur_item) ).start()
                elif ('/sp/2/' in addr):
                    cur_item = {'kode_wilayah': addr.split('/')[-1], 'id_level_wilayah': 2 }
                    URL = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah={}&kode_wilayah={}&semester_id=20191'.format( cur_item['id_level_wilayah'], cur_item['kode_wilayah'].strip().rstrip() )
                    Thread(target = self.parse_third, args = (URL, cur_item) ).start()
                elif ('/sp/3/' in addr):
                    cur_item = {'kode_wilayah': addr.split('/')[-1], 'id_level_wilayah': 3 }
                    URL = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah={}&semester_id=20191&bentuk_pendidikan_id={}'.format( cur_item['kode_wilayah'].strip().rstrip(), 'sd')
                    Thread(target = self.parse_forth, args = (URL, cur_item) ).start()
                elif 'sekolah' in addr:
                    cur_item = {'sekolah_id_enkrip': addr.split('/')[-1] }
                    Thread(target = self.parse_page, args = (addr, cur_item) ).start()

            while (1):
                try:
                    time.sleep(0.4)
                except:
                    os.kill(os.getpid(), 15)

        else:
            self.parse_first()


    def parse_first(self):
        URL = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=0&kode_wilayah=000000&semester_id=20191'
        data = json.loads( urlopen(URL).read().decode('utf-8') )

        with open('data/sp.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        for item in data:
            if ('id_level_wilayah' in item and 'kode_wilayah' in item and item['id_level_wilayah'] == 1 ):
                URL =  'http://dapo.dikdasmen.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah={}&kode_wilayah={}&semester_id=20191'.format( item['id_level_wilayah'], item['kode_wilayah'].strip().rstrip() )
                

                while (self.thread_count >= 10):
                    try:
                        time.sleep(0.1)
                    except:
                        os.kill(os.getpid(), 15)

                self.thread_count += 1                
                Thread(target = self.parse_second, args = ( URL, item ) ).start()
                try:
                    time.sleep(0.4)
                except:
                    os.kill(os.getpid(), 15)

    def parse_second(self, URL, cur_item):
        self.log('Parsing {}-{}.json'.format( cur_item['id_level_wilayah'], cur_item['kode_wilayah'].strip().rstrip() ))
        try:
            data = json.loads( urlopen(URL, timeout=10).read().decode('utf-8') )
        except:
            self.thread_count -=1
            return

        try:
            with open('data/{}-{}.json'.format( cur_item['id_level_wilayah'], cur_item['kode_wilayah'].strip().rstrip() ), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            for item in data:
                if ('id_level_wilayah' in item and 'kode_wilayah' in item and item['id_level_wilayah'] == 2):
                    URL =  'http://dapo.dikdasmen.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah={}&kode_wilayah={}&semester_id=20191'.format( item['id_level_wilayah'], item['kode_wilayah'].strip().rstrip() )
                    self.parse_third( URL, item )
            self.DONE[URL] = 1

        except Exception as err:
            self.log(str(err), 'warning')

        self.thread_count -= 1

    def parse_third(self, URL, cur_item):
        if URL in self.DONE:
            self.log("Skipping {}, already done".format(URL) )
            return

        self.log('Parsing {}-{}.json'.format( cur_item['id_level_wilayah'], cur_item['kode_wilayah'].strip().rstrip() ))
        try:
            data = json.loads( urlopen(URL, timeout=10).read().decode('utf-8') )
        except:
            return

        with open('data/{}-{}.json'.format( cur_item['id_level_wilayah'], cur_item['kode_wilayah'].strip().rstrip() ), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        for item in data:
            if ('id_level_wilayah' in item and 'kode_wilayah' in item and item['id_level_wilayah'] == 3):
                which = ['sd', 'smp', 'sma', 'smk', 'slb']
                for temp in which:
                    URL = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah={}&semester_id=20191&bentuk_pendidikan_id={}'.format( item['kode_wilayah'].strip().rstrip(), temp )
                    self.parse_forth( URL, item, temp )
        self.DONE[URL] = 1

    def parse_forth(self, URL, cur_item, which = 'sd'):
        if URL in self.DONE:
            self.log("Skipping {}, already done".format(URL) )
            return

        self.log('Parsing {}-3-{}.json'.format( which, cur_item['kode_wilayah'].strip().rstrip() ))
        try:
            data = json.loads( urlopen(URL, timeout=10).read().decode('utf-8') )
        except:
            return 

        with open('data/{}-3-{}.json'.format( which, cur_item['kode_wilayah'].strip().rstrip() ), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        for item in data:
            if ('sekolah_id_enkrip' in item):
                URL = 'http://dapo.dikdasmen.kemdikbud.go.id/sekolah/{}'.format( item['sekolah_id_enkrip'].strip().rstrip() )
                self.parse_page( URL, item )
        self.DONE[URL] = 1

    def parse_temp(self, temp):
        dic = {}
        for i in range(len(temp)):
            key = temp[i].xpath('./strong/text()')
            value = temp[i].xpath('./text()')

            if (len(key) and len(value)):
                key = key[0].replace(':', '').strip().rstrip()
                key = key.replace(' ', '_').lower()
                value = value[0].strip().rstrip()
                dic[key] = value
        return dic

    def parse_page(self, URL, cur_item):
        if URL in self.DONE:
            self.log("Skipping {}, already done".format(URL) )
            return

        OLD_URL = URL
        try:
            data = urlopen(URL, timeout=10).read()
        except:
            return
        URL = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/sekolahDetail?semester_id=20182&sekolah_id={}'.format( cur_item['sekolah_id_enkrip'].strip().rstrip() )
        try:
            rekapitulasi = json.loads( urlopen(URL, timeout=10).read().decode('utf-8') )
        except:
            return


        if ( len(rekapitulasi) ):
            temp = rekapitulasi[0]
            rekapitulasi = {}
            rekapitulasi['rekapitulasi'] = {}

            keys = ['ptk', 'ptk_laki', 'ptk_perempuan', 'ptk_valid', 'pd_laki', 'pd_perempuan', 'pd_valid', 'pegawai', 'pegawai_laki', 'pegawai_perempuan', 'prasarana_valid'  ]
            rekapitulasi['rekapitulasi']['data_ptk_dan_pd'] = {}
            for key in temp:
                if (key in keys): rekapitulasi['rekapitulasi']['data_ptk_dan_pd'][key] = temp[key]

            keys = ['jml_rk','jml_perpus','jml_lab','jml_wastafel']
            rekapitulasi['rekapitulasi']['data_sarpras'] = {}
            for key in temp:
                if (key in keys): rekapitulasi['rekapitulasi']['data_sarpras'][key] = temp[key]

            keys = ['a_sabun_air_mengalir','jml_jamban_digunakan','jml_jamban_tidak_digunakan','jml_wastafel','kecukupan_air','ketersediaan_air','memproses_air','minum_siswa','siswa_bawa_air','sumber_air_str', 'tipe_jamban']
            rekapitulasi['rekapitulasi']['data_sanitasi'] = {}
            for key in temp:
                if (key in keys): rekapitulasi['rekapitulasi']['data_sanitasi'][key] = temp[key]

            rekapitulasi['rekapitulasi']['data_rombongan_belajar'] = {}
            for key in temp:
                if (key.startswith('pd_kelas')): rekapitulasi['rekapitulasi']['data_rombongan_belajar'][key] = temp[key]


        obj = html.fromstring(data)
        
        images = {'images': [] }

        link = obj.xpath('(//div[@class="profile-userbuttons"]/a)[1]/@href')
        if (len(link)):
            try:
                data2 = urlopen(link[0], timeout=10).read()
                obj2 = html.fromstring(data2)
                images['images'] = obj2.xpath('//img[@data-u="image"]/@src')
            except:
                pass


        profil = { 'profil': {} }
        kontak = { 'kontak': {'kontak_utama': {} }  }

        temp = obj.xpath('//div[@class="profile-usermenu"]//li//text()')
        temp = [ i.replace('\n', '').strip().rstrip() for i in temp if i.replace('\n', '').strip().rstrip() ]
        i = 0
        while (i < len(temp) ):
            if (':' in temp[i] and i+1 < len(temp) ):
                if (':' in temp[i+1]):
                    profil['profil'][ temp[i].replace(':', '').strip().rstrip().lower() ] = ''
                else:
                    profil['profil'][ temp[i].replace(':', '').strip().rstrip().lower() ] = temp[i+1]
                    i += 1
            i+=1

        temp1 = obj.xpath('(//div[@id="profil"]//div[@class="panel panel-info"])[1]//p')
        profil['profil']['identitas_sekolah'] = self.parse_temp(temp1)
        temp2 = obj.xpath('(//div[@id="profil"]//div[@class="panel panel-info"])[2]//p')
        profil['profil']['data_lengkap'] = self.parse_temp(temp2)
        temp3 = obj.xpath('(//div[@id="profil"]//div[@class="panel panel-info"])[3]//p')
        profil['profil']['data_rinci'] = self.parse_temp(temp3)
        
        temp = obj.xpath('//div[@id="kontak"]//p')
        kontak['kontak']['kontak_utama'] = self.parse_temp(temp)

        NPSN = '-1'
        if ('npsn' in profil['profil']['identitas_sekolah'] ):
            NPSN = profil['profil']['identitas_sekolah']['npsn']

        if (NPSN != '-1' and NPSN not in os.listdir('data/schools') ):
            os.mkdir('data/schools/{}'.format(NPSN) )
            
            self.log('Saved school {}'.format( NPSN ) )

            with open('data/schools/{}/profil.json'.format( NPSN ), 'w') as f:
                json.dump(profil, f, ensure_ascii=False, indent=4)
            with open('data/schools/{}/kontak.json'.format( NPSN ), 'w') as f:
                json.dump(kontak, f, ensure_ascii=False, indent=4)
            with open('data/schools/{}/rekapitulasi.json'.format( NPSN ), 'w') as f:
                json.dump(rekapitulasi, f, ensure_ascii=False, indent=4)
            with open('data/schools/{}/images.json'.format( NPSN ), 'w') as f:
                json.dump(images, f, ensure_ascii=False, indent=4)

        self.DONE[OLD_URL] = 1

        f = open('data/done.json', 'w')
        f.write( str(self.DONE) )
        f.close()

    def log(self, msg, state = 'info'):
        print (state.upper() + ": " + str(msg) )

if __name__ == '__main__':
    obj = Main()