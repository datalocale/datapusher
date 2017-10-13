import os

import ckanserviceprovider.web as web

import jobs

# check whether jobs have been imported properly
assert(jobs.push_to_datastore)


def setup_sentry(app):
    try:
        from raven.contrib.flask import Sentry
    except ImportError:
        print('missing raven[flask] package, no sentry support')
        return
    # dsn information will be looked for in SENTRY_DSN environment variable.
    sentry = Sentry()
    sentry.init_app(app)


def serve():
    web.init()
    setup_sentry(web.app)
    web.app.run(web.app.config.get('HOST'), web.app.config.get('PORT'))


def serve_test():
    web.init()
    return web.app.test_client()


def main():
    import argparse

    argparser = argparse.ArgumentParser(
        description='Service that allows automatic migration of data to the CKAN DataStore',
        epilog='''"He reached out and pressed an invitingly large red button on a nearby panel.
                The panel lit up with the words Please do not press this button again."''')

    argparser.add_argument('config', metavar='CONFIG', type=file,
                           help='configuration file')
    args = argparser.parse_args()

    os.environ['JOB_CONFIG'] = os.path.abspath(args.config.name)
    serve()

if __name__ == '__main__':
    main()
