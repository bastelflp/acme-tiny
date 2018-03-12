import ftplib
import json
import logging

def upload_ftp(fullfile, token):

    log = logging.getLogger(__name__)

    # load FTP credentials
    with open('./credentials/ftp.json', 'r') as ftp_file:
        ftp_cfg = json.load(ftp_file)

    # load FTP path
    with open('./path_tmp.json', 'r') as domain_file:
        domains = json.load(domain_file)

    # connect to FTP server
    log.info('Connecting to FTP server')
    ftp = ftplib.FTP_TLS(ftp_cfg['url'], ftp_cfg['user'], ftp_cfg['pwd'])
    root_dir = ftp.pwd()

    # navigate to base folder for well_known challenge (has to exist on the FTP server)
    for path in domains['path']:
        ftp.cwd(root_dir + domains['path'][path] + '/.well-known/acme-challenge')

        # upload challenge file and .htaccess file
        log.info('Upload file: {}'.format(fullfile))
        with open(fullfile, 'rb') as challenge_file:
            ftp.storbinary(cmd='STOR {}'.format(token), fp=challenge_file)
        with open('.\well-known\.htaccess', 'rb') as ht_file:
            ftp.storbinary(cmd='STOR {}'.format('.htaccess'), fp=ht_file)

    # close FTP
    ftp.close()

if __name__ == '__main__':
    upload_ftp('./test.txt', 'text.txt')
