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
		...
		<table id="constants">
			...
				<tr class="apilevel-*" data-version-added="*">
					...
						<td width="100%">
							<a href="...">
								<span>PERMISSION_NAME</span>
							</a>
						</td>
				</tr>
				...
		</table>
	"""
	tr_unique_attribute="data-version-added"
	table=soup.find("table",id="constants")
	max_sdk_version=""

	for tr in table.find_all("tr"):
		if tr.has_attr(tr_unique_attribute):
			links=tr.find_all("a")
			if len(links)>=2:
				# First element must be "String"
				name=links[1].text
				api_level=tr[tr_unique_attribute]
				params={
					"name":name,
					"maxSdkVersion":max_sdk_version,
					"apiLevel":api_level
				}
				permissions.append(params)
		
	
	return permissions

def main():
	for permission in get_all_permissions():
		name=permission["name"]
		max_sdk_version=permission["maxSdkVersion"]
		apiLevel=permission["apiLevel"]
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

