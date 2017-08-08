#coding=utf-8
"""
引用自GitHub@kwsy的开源大规模预料新词发现算法
具体请参阅https://github.com/kwsy
"""
'''
Created on 2016-1-23

@author: kwsy
'''

import os
import hibiscusTools
import codecs
from xlwt import Workbook
from audioop import reverse
import sys  

class Hibiscus():
    def analyseNovel(self,content):
        content = content
        txtlist = hibiscusTools.getAllChineseCharacters(content)
        self.novelInfo = {}
        index = 0
        for txt in txtlist:
            itemlst = hibiscusTools.getLatentword(txt, index)
            index = index+len(txt)
            for item in itemlst:
                word = item['word']
                if not word in self.novelInfo:
                    self.novelInfo[word] = {'leftLst':[],'rightLst':[],'wordindexLst':[],'count':0,'word':word}
                if not item['left']==None:
                    self.novelInfo[word]['leftLst'].append(item['left'])
                if not item['right']==None:
                    self.novelInfo[word]['rightLst'].append(item['right'])
                self.novelInfo[word]['wordindexLst'].append(item['wordindex'])
                self.novelInfo[word]['count'] = self.novelInfo[word]['count']+1
                
        self.charCount = index
        self.calculte()
        result=self.outResult()
        return result
        
    def outResult(self):
        wb = Workbook()
        table = wb.add_sheet(u'新词')
        table.write(0,0,u'单词')
        table.write(0,1,u'出现次数')
        table.write(0,2,u'凝结度')
        table.write(0,3,u'自由度')
        lst = []
        for k,v in self.novelInfo.items():
            if v['count']>30 and len(k)>1 and v['solidification']>50 and v['freedom']>1: #原来为30,50,3
                lst.append(v)
        
        lst = sorted(lst,key=lambda x:x['count'],reverse=True)

        count=0;
        result=[]
        for index,item in enumerate(lst):
            result.append(item['word'])
            count+=1
            if count==5:
                break
        return  result
        
    def calculte(self):
        for word,info in self.novelInfo.items():
            self.novelInfo[word]['solidification']= self.getSolidification(word)       
            self.novelInfo[word]['freedom'] = self.getFreedom(self.novelInfo[word])
    def getFreedom(self,wordinfo):
        leftfreedom = hibiscusTools.calculateFreedom(wordinfo['leftLst'])
        rightfreedom = hibiscusTools.calculateFreedom(wordinfo['rightLst'])
        if leftfreedom<rightfreedom:
            return leftfreedom
        return rightfreedom
    def getSolidification(self,word): 
        
        splitLst = hibiscusTools.splitWord(word)
        wordcount = self.novelInfo[word]['count']
        probability = float(wordcount)/float(self.charCount)
        min = 10000000
        for item in splitLst:
            left,right = item[0],item[1]
            leftcount,rightcount = self.novelInfo[left]['count'],self.novelInfo[right]['count']
            
            Togetherprobability = probability/((float(rightcount)/float(self.charCount))*(float(leftcount)/float(self.charCount)))
            if Togetherprobability<min:
                min = Togetherprobability
        return min


def excute(name):
    hibi = Hibiscus()
	
if __name__ == '__main__':
    excute()