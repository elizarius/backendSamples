import csv
import json

#from dbhelper import db_helper

selected_tables_columns = {
    'asset_inventory_asset':
        ['id',
         'asset_owner',
         'ip_address',
         'name',
         'description',
         'port',
         'criticality',
         'created_at',
         'origin',
         'log_identifier',
         'asset_type_id',
         'parent_id'],
    'asset_inventory_cloudcredentials':
        ['id',
         'name'],
    'sync_ecm':
        ['name',
         'address',
         'tenant',
         'vdc'],
}



def read_config_file(path):
    print("Reading %s... {}.".format(path))
    with open(path, 'r') as f:
        metadata = f.read()
        config = json.loads(metadata)
        #config = json.dumps(metadata)
        return config

def main():
    path = "/home/ealexel/samples/pythonExample/black_listed.json"
    cred = 'asset_inventory_cloudcredentials'
    config = read_config_file(path)
    config1 = json.dumps(config)
    print("Config: {}.".format(config))
    print("Config1: {}.".format(config1))

    # Aelz: dumped object cannot be accessed as dictionary because represent string.
    #print("Config1[]: {}.".format(config1.get('inventory_cloud_credentials',[] )))
    print("Config1[]: {}.".format(config['asset_inventory_cloudcredentials']))

    #if cred in config:
    #    credentials = config.get(cred, [])
    #    print("credentials: {}.".format(credentials))
    #    print("cred 1 : {}.".format(json.dumps(credentials)))

    #print("*********************************")
    #print("Internal list: {}.".format(selected_tables_columns[cred]))


    #cr_list = config['asset_inventory_cloudcredentials']
    #print("cr_list: {}.".format(cr_list))

    #for credo in credentials:
    #    print("credential: {}.".format(credo))



#   write_db_contents_to_csv()

if __name__ == '__main__':
    main()


