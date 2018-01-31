# -*- coding: utf-8 -*-

"""
    Lastship Add-on (C) 2017
    Credits to Exodus and Covenant; our thanks go to their creators

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import urllib
import urlparse
import re
import base64
import hashlib


from resources.lib.modules import pyaes
from resources.lib.modules import cfscrape



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['hd-streams.org']
        self.base_link = 'https://hd-streams.org/'
        self.movie_link= self.base_link + 'movies?perPage=54'
        self.movie_link= self.base_link + 'seasons?perPage=54'
        self.search=self.base_link + 'search?q=%s&movies=true&seasons=true&actors=false&didyoumean=false'
        self.scraper=cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            print "print movie entry to search", title, imdb
            url = self.__search(imdb)
            print "print movie return url", url
            
            return url
            
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            
            return 
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            return 
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources

            sHtmlContent=self.scraper.get(url).content
            
            pPattern = "loadStream[^>]'([^']+)', '([^']+)', '([^']+).*?"
            pPattern += '>.*?>([^"]+)</v-btn>'
            aResult = re.compile(pPattern, re.DOTALL).findall(sHtmlContent)
            
            pattern = '<meta name="csrf-token" content="([^"]+)">'
            string = str(sHtmlContent)
            token = re.compile(pattern, flags=re.I | re.M).findall(string)
            
            # 1080p finden
            if '1080p' in string:
                print "Qualität 1080p"
                q='1080p'
      
            for e, h, sLang, sName in aResult:
                link=self.__getlinks(e,h,sLang,sName,token,url)
                
                # hardcoded, da Qualität auf der Webseite inkorrekt beschrieben ist unnd sName.strip() problem liefert aufgrund webseite. nxload kanndamit unterdrückt werden
                
                if q=='1080p' and e=='1':
                    if 'openload' in link:
                        sources.append({'source': 'openload.com', 'quality': '1080p', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                    elif 'streamango' in link:
                        sources.append({'source': 'streamango.com', 'quality': 'HD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                    elif 'nxload' in link:
                        sources.append({'source': 'nxload.com', 'quality': '1080p', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                    elif 'streamcloud' in link:
                        sources.append({'source': 'streamcloud.com', 'quality': 'SD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                else:
                    if 'openload' in link:
                        sources.append({'source': 'openload.com', 'quality': 'HD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                    elif 'streamango' in link:
                        sources.append({'source': 'streamango.com', 'quality': 'HD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                    elif 'nxload' in link:
                        sources.append({'source': 'nxload.com', 'quality': 'HD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})
                    elif 'streamcloud' in link:
                        sources.append({'source': 'streamcloud.com', 'quality': 'SD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def __getlinks(self,e, h, sLang, sName,token,url):
            #print "print def get links self,e, h, sLang, sName,token, url", self,e, h, sLang, sName, token, url
            url=url+'/stream'
            # hardcoded german language
            params={'e':e,'h':h,'lang':'de'}
            sHtmlContent=self.scraper.post(url,headers={'X-CSRF-TOKEN':token[0],'X-Requested-With':'XMLHttpRequest'},data=params).content
                        
            pattern = 'ct[^>]":[^>]"([^"]+).*?iv[^>]":[^>]"([^"]+).*?s[^>]":[^>]"([^"]+).*?e"[^>]([^}]+)'
            
            aResult = re.compile(pattern, re.DOTALL).findall(sHtmlContent)
            
            token=base64.b64encode(token[0])
           
            for ct, iv, s, e in aResult:                
                ct = re.sub(r"\\", "", ct[::-1])
                s = re.sub(r"\\", "", s)         
                
                
            sUrl2 = self.__evp_decode(ct, token, s.decode('hex'))            
            fUrl=sUrl2.replace('\/', '/').replace('"', '')       
                
            return fUrl



    def resolve(self, url):
        return url

    def __search(self, imdb):
        try:
            sHtmlContent=self.scraper.get(self.base_link).content
            #print "print hdstreams.org shtml entry", sHtmlContent
            pattern = '<meta name="csrf-token" content="([^"]+)">'
            string = str(sHtmlContent)
            token = re.compile(pattern, flags=re.I | re.M).findall(string)
            #print "print hdstreams.org shtml entry token", token[0]
            # first iteration of session object to be parsed for search
            #sHtmlContent=self.scraper.get(self.search % imdb).content
            #sHtmlContent=self.scraper.get(self.search % imdb).content
            sHtmlContent=self.scraper.get(self.search % imdb,headers={'X-CSRF-TOKEN':token[0],'X-Requested-With':'XMLHttpRequest'}).text
               
            #print "print hdstreams.org shtml", sHtmlContent
            pattern = '"title":"([^"]+).*?"url":"([^"]+).*?src":"([^"]+)'
            aResult = re.compile(pattern, re.DOTALL).findall(sHtmlContent)
            
            for sName, sUrl, sThumbnail in aResult:
                url= sUrl.replace('\/', '/')
                
            return url
        except:
            return

    def __get_ajax_object(self, html=None):
        try:
            r = client.request(self.base_link) if not html else html
            r = re.findall('ajax_object\s*=\s*({.*?});', r)[0]
            r = json.loads(r)
            return r
        except:
            return {}
