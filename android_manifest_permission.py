#!/usr/bin/python
#	-*- coding:utf-8 -*-
"""
	BeautifulSoup: http://kondou.com/BS4/
"""
import re
import sys
import urllib
from bs4 import BeautifulSoup

def get_all_permissions():
	permissions=[]
	url_user_permissions="https://developer.android.com/reference/android/Manifest.permission"
	soup=BeautifulSoup(urllib.urlopen(url_user_permissions),"html.parser")

	"""
		<div class="api apilevel-*" data-version-added="*">
			<h3 class="api-name">PERMISSION NAME</h3>
			...
				<p>Protection level: A|B<p>
		</div>
	"""
	divs=soup.find_all("div", class_="api")
	max_sdk_version=None
	for div in divs:
		if div.has_attr("data-version-added"):
			p=div.find("p",text=re.compile("Protection level:"))
			protection_levels=[]
			if p:
				text=p.text.split(":")[1].strip()
				protection_levels=text.split("|")
			name=div.find("h3", class_="api-name").text
			api_level=div["data-version-added"]
			params={
				"name":name,
				"maxSdkVersion":max_sdk_version,
				"apiLevel":api_level,
				"protectionLevel":protection_levels
			}
			permissions.append(params)
		
	return permissions

def main():
	for permission in get_all_permissions():
		name=permission["name"]
		max_sdk_version=permission["maxSdkVersion"]
		api_level=permission["apiLevel"]
		"""
			Syntax: <uses-permission android:name="string" android:maxSdkVersion="integer" />

				site: https://developer.android.com/guide/topics/manifest/uses-permission-element
		"""
		template="<uses-permission android:name=\"{}\" {}/>"
		print template.format(
				name,
				"android:maxSdkVersion=\"{}\"".format(max_sdk_version) if max_sdk_version else ""
			)

if __name__=="__main__":
	main()

