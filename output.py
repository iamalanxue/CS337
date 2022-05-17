import json 

def output(dictionary):
    for key in dictionary:
        print(key,":",dictionary[key])
    return


def jsonout(dictionary):
    result=json.dumps(dictionary) 
    print(result)
    return result

if __name__ == '__main__':
    output()
    jsonout()
