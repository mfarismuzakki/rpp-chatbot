import re

def createQuery(teks):
    t = teks.upper()
    kb ={
        ".*TATA CARA SHOLAT RAWATIB.*":'''
        MATCH (a:Amalan {name:"rawatib"})-[:tata_cara]->(tc:TataCara) RETURN tc
        ''',
        ".*SHAUM RAMADHAN HUKUM.*":'''
        MATCH (a:Amalan {name:"shaum"})-[w:amalan_wajib]->(f:Farduain {name:"ramadhan"}) RETURN w
        ''',
        ".*SOLAT JENAZAH.*":'''
        MATCH (a:Amalan {name:"solat"})-[afk:amalan_fardu_kifayah]->(fk:FarduKifayah) RETURN afk
        ''',
        ".*BAYAR ZAKAT FITRAH.*":'''
        MATCH (a:Amalan {name:"fitrah"})-[:tata_cara]->(tc:TataCara) RETURN tc
        ''',
        ".*QIYAMULAIL.*":'''
        MATCH (a:Amalan {name:"solat"})-[as:amalan_sunnah]->(s:Sunnah{detail:"qiyamul lail"}) RETURN as
        ''',
        ".*HUKUM (SOLAT|SHOLAT) DHUHA.*":'''
        MATCH (a:Amalan {name:"solat"})-[b:amalan_sunnah]->(s:Sunnah) RETURN b
        ''',
        ".*HUKUM (SOLAT|SHOLAT).*":'''
        MATCH (a:Amalan {name:"solat"})-[:jenis_amalan]->(j:JenisAmalan) RETURN j
        ''',
        ".*(SHOLAT|SOLAT).*ADA APA.*":'''
        MATCH (a:Amalan {name:"solat"})-[:jenis_amalan]->(j:JenisAmalan)
        MATCH (a)-[:amalan_wajib]->(f:Farduain)
        MATCH (a)-[:amalan_sunnah]->(s:Sunnah)
        MATCH (a)-[:amalan_fardu_kifayah]->(fk:FarduKifayah)
        RETURN j,f,fk
        ''',
        ".*SHAUM.*ADA APA.*":'''
        MATCH (a:Amalan {name:"shaum"})-[:jenis_amalan]->(j:JenisAmalan)
        MATCH (a)-[:amalan_wajib]->(f:Farduain)
        MATCH (a)-[:amalan_sunnah]->(s:Sunnah)
        RETURN j,f
        ''',
        ".*TATA CARA SHAUM YAUMUL BIDH.*":'''
        MATCH (a:Amalan {name:"yaumul bidh"})-[:tata_cara]->(tc:TataCara) RETURN tc
        '''
    }
    for key in kb:
        m = re.match(key, t)
        if m:
            answer = kb[key]
            len_groups = len(m.groups())
        
            if (len_groups == 0):
                return answer
            else:
                X = m.group(1)
                answer = answer.replace("X",X)
                if " ME " in answer:
                    answer = answer.replace(" ME "," YOU ")
                return answer
    return m