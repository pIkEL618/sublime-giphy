import sublime
import sublime_plugin
import http
import json
import urllib

class GiphyCommand(sublime_plugin.TextCommand):
	
	giphy_api_key = "" #fill in your api-key here

	def get_gif_with_tag(self, tag):
		conn = http.client.HTTPSConnection('api.giphy.com')
		conn.request("GET", "/v1/gifs/random?api_key=" + self.giphy_api_key + "&tag=" + urllib.parse.quote(tag))
		response = conn.getresponse().read().decode('utf-8')
		j = json.loads(response)
		if not j["data"]:
			return None
		url = j["data"]["image_url"]
		return url

	def run(self, edit):
		for region in self.view.sel():
			tag = self.view.substr(region).split("\n")[0]
			url = self.get_gif_with_tag(tag)
			if not url:
				print("Could not find a gif with tag: \"" + tag + "\". Will fallback to a random gif.")
				url = self.get_gif_with_tag("")
				tag = "random"
			if not tag:
				tag = "random"
			self.view.replace(edit, region, "!["+tag+" gif](" + url + ")")
