from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/',)

# Create server
with SimpleXMLRPCServer(('localhost', 8081),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register a function under a different name
    #server.register_function(adder_function, 'add')

    # Register a function under a different name
    def arroser(etat):
        if etat == "ouverture":
            print("Arrosage en cours")
            return True
        if etat == "fermeture":
            print("Arrosage terminé")
            return False
    server.register_function(arroser, 'arroser')

    # Run the server's main loop
    server.serve_forever()