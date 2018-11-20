# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class TestDev256ComPipeline( object ):
    def __init__( self ):
        self.file = None
        self.csvWriter = None
        pass

    def open_spider( self, spider ):
        self.file = open( "pages.csv", "w" )
        self.csvWriter = csv.writer( self.file, delimiter = "\t", quotechar = "", quoting = csv.QUOTE_NONE )  # csv.QUOTE_MINIMAL
        self.csvWriter.writerow( [ "url", "status", "referer", "title", "h1", "ahref" ] )

    def close_spider( self, spider ):
        self.file.close()

    def process_item( self, item, spider ):
        self.csvWriter.writerow( [ item[ "url" ], item[ "status" ], item[ "referer" ], item[ "title" ], item[ "h1" ], item[ "ahref" ] ] )
        # self.csvWriter.writerow( [ "h1", "h2" ] )
        return item
