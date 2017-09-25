
import os
import json
import numpy as np
import pandas as pd
import urllib
import zipfile

_pack = [ 'code', 'pack_code', 'position', 'quantity' ]
_faction = [ 'side_code', 'faction_code' ]
_deckbuilding = [ 'faction_cost', 'deck_limit' ]
_types = [ 'type_code', 'keywords', ]
_id = [ 'minimum_deck_size', 'influence_limit', 'base_link' ]
_mechanics = [ 'text', 'cost', 'trash_cost', 'uniqueness' ]
_agenda = [ 'advancement_cost', 'agenda_points' ]
_special = [ 'memory_cost', 'strength', 'num_subs' ]
_flavor = [ 'flavor', 'illustrator' ]

_column_order = _pack + _faction + _deckbuilding + _types + _id + _mechanics + _agenda + _special + _flavor

json_dir = "data/"
netrunner_data_dir = json_dir + 'netrunner-cards-json-master/'

def get_cards_df():

    if not os.path.exists( netrunner_data_dir ):
        os.makedirs( json_dir )
        url = 'https://github.com/Alsciende/netrunner-cards-json/archive/master.zip'
        f, _ = urllib.request.urlretrieve( url )
        zipfileobject = zipfile.ZipFile( f )
        zipfileobject.extractall( json_dir )

    pack_data_dir = netrunner_data_dir + 'pack/'
    data = []
    for f in filter( lambda x : x.endswith( ".json" ), os.listdir( pack_data_dir ) ):
        #print( "loading " + f )
        data += json.load( open( pack_data_dir + f, 'r' ) )

    df = pd.DataFrame( data )
    add_subroutines_column(df)
    df = df.set_index( ['title'] )
    df = df.reindex( columns = _column_order )
    df = df.sort_values( by='code' )
    #df = df.groupby( 'type_code' )
    #df.sort_index( inplace=True )

    return df

def add_subroutines_column(df):
    subs = pd.Series( [ num_subroutines( x ) for x in df['text'] ] )
    df['num_subs'] = subs

def num_subroutines(cardtext):
    if not isinstance( cardtext, str ):
        return np.nan
    n = len( cardtext.split("[subroutine]") ) - 1
    if n:
        return n
    return np.nan


if __name__ == '__main__':
    cards_df = get_cards_df()
    print( cards_df.head() )
