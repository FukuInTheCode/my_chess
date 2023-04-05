import pickle
 
ls = {
    1: {
        
    },
    -1:{
        
    }
}
 
def save_object(obj):
    try:
        with open("opdata.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

