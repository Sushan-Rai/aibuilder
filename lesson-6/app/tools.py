from langchain.tools import tool



@tool
def search_it_docs(query:str):

    """
    Search IT documentation once.
    """

    docs = {

        "vpn":
        "Restart VPN client and verify credentials.",


        "password":
        "Reset password using employee portal."

    }


    for key,value in docs.items():

        if key in query.lower():

            return value


    return "No documentation found."