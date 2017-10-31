# flickrsmartsync_oauth

Upload, download or sync photos and videos to flickr.

## Install

Download flickrsmartsync_oauth:

```sh
> pip install git+https://github.com/titimoi/flickrsmartsync_oauth
> pip install flickrapi
```

Create your own personal Flickr API keys:
```sh
> https://www.flickr.com/services/apps/create/apply
```

Add api_key and api_secret to flickrsmartsync_oauth/flickrsmartsync_oauth/config.py:
```sh
  api_key = u'<API_KEY>'
  api_secret = u'<API_SECRET>'
```

Run the install script:
```sh
> python setup.py install
```

## Example Usage

Authenticate manually and upload all photos and vidoes in current folder and all sub-folders:
```sh
> flickrsmartsync_oauth --manual-auth
```

Upload all photos and vidoes in current folder and all sub-folders once authenticated at least once before :
```sh
> flickrsmartsync_oauth
```

## Acknowledgments

flickrsmartsync_oauth is an extension of [flickrsmartsync](https://github.com/faisalraja/flickrsmartsync) written by Faisal Raja.
flickrsmartsync_oauth includes [flickrapi](https://github.com/sybrenstuvel/flickrapi) version 2.3 supporting oauth written by Sybren Stuvel.

## License

MIT
