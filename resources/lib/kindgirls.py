from BeautifulSoup import BeautifulSoup
import requests

class KindGirls():
	
	main_url = 'http://www.kindgirls.com/%s'
	photo_url = main_url % ('photo-archive')
	girls_url = main_url % ('girls')

	def GetMonths(self):
		HTML = self.GetHTML(self.photo_url)
		Months = None
		
		if(HTML):
			Soup = BeautifulSoup(HTML)
			Select = Soup.find('select', {'name': 's'});
			
			if(Select):
				Months = []
				Options = Select.findAll('option')
				
				for Option in Options:				
					Months.append({'Date': Option['value'], 'Name': Option.text})
			
		return Months

	def GetCountries(self):
		HTML = self.GetHTML(self.girls_url)
		Countries = None
		
		if(HTML):
			Soup = BeautifulSoup(HTML)
			Select = Soup.find('select', {'name': 'c'});
			
			if(Select):
				Countries = []
				Options = Select.findAll('option')
				
				for Option in Options:
					if(int(Option['value']) != 0):
						Countries.append({'Id': int(Option['value']), 'Name': Option.text})
			
		return Countries
		
	def GetLetters(self):
		HTML = self.GetHTML(self.girls_url)
		Letters = None
		
		if(HTML):
			Soup = BeautifulSoup(HTML)
			Select = Soup.find('select', {'name': 'i'});
			
			if(Select):
				Letters = []
				Options = Select.findAll('option')
				
				for Option in Options:
					if(Option['value'] != '0'):
						Letters.append({'Id': Option['value'], 'Name': Option.text})

		return Letters

	def GetMonthGalleries(self, Month):
		month_url = self.photo_url + '?s=%s' % (Month)
		HTML = self.GetHTML(month_url)
		MonthGalleries = None

		if(HTML):
			Soup = BeautifulSoup(HTML)
			Galleries = Soup.findAll('div', {'class': 'gal_list'})

			if(Galleries):
				MonthGalleries = []

				for Gallery in Galleries:
					Link = Gallery.find('a')
					Img = Gallery.find('img')

					MonthGalleries.append({
						'Url': self.main_url % (Link['href'].strip('/')),
						'Title': Img['alt'],
						'Img': Img['src']
					})

		return MonthGalleries

	def GetGirls(self, letter = None, country = None):
		
		if(letter is None):
			Url = self.girls_url + '?c=%s' % (country)
		else:
			Url = self.girls_url + '?i=%s' % (letter)
		
		HTML = self.GetHTML(Url)
		Girls = None

		if(HTML):
			Soup = BeautifulSoup(HTML)
			Models = Soup.findAll('div', {'class': 'model_list'})
			
			if(Models):
				Girls = []
				
				for Model in Models:
					Link = Model.find('a')
					Img = Model.find('img')
					
					Girls.append({
						'Url': self.main_url % (Link['href'].strip('/')),
						'Title': Img['alt'],
						'Img': self.main_url % (Img['src'].strip('/')),
					})

		return Girls

	def GetGirlGalleries(self, Url):
		HTML = self.GetHTML(Url)
		GirlGalleries = None

		if(HTML):
			Soup = BeautifulSoup(HTML)
			Galleries = Soup.findAll('div', {'class': 'gal_list'})

			if(Galleries):
				GirlGalleries = []

				for Gallery in Galleries:
					Link = Gallery.find('a')
					Img = Gallery.find('img')

					GirlGalleries.append({
						'Url': self.main_url % (Link['href'].strip('/')),
						'Title': Link['title'],
						'Img': Img['src']
					})

		return GirlGalleries

	def GetGallery(self, Url):
		HTML = self.GetHTML(Url)
		Gallery = None

		if(HTML):
			Soup = BeautifulSoup(HTML)
			Images = Soup.findAll('div', {'class': 'gal_list'})

			if(Images):
				Gallery = []

				for Image in Images:
					Img = Image.find('img')
					Link = Image.findAll('a')[1]

					Gallery.append({
						'Title': Img['title'],
						'ThumbUrl': Img['src'],
						'PhotoUrl': Link['href']
					})

				Girls = Soup.find('div', {'id': 'up_izq'})
				GirlsLink = Girls.findAll('a')
				
				if(Girls):
					
					for Girl in GirlsLink:
						Gallery.append({
							'Name': Girl.text,
							'Url': self.main_url % (Girl['href'].strip('/')),
						})
	
		return Gallery

	def GetHTML(self, url):
		HTML = None
		Headers = {
			'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
			'referer': self.main_url % ('')
		}
		
		r = requests.get(url, headers = Headers)
		
		if(r.status_code == 200):
			HTML = r.text.encode('utf-8')

		return HTML
