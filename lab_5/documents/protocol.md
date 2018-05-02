### Protocolul de comunicare intre client si server

**Formatul mesajelor**

- Comenzile de la client încep cu /
- Numele comenzii poate contine A-Za-z0-9_ De exemplu: /help
- Daca comanda accepta parametri, atunci dupa comanda urmeaza spatiu si restul datelor. Exemplu: /hello John
- Daca serverul primeste o comanda invalida - se raspunde cu un mesaj informativ.

**Comenzile suportate de server**

    * /dice - virtually role the dice
    * /flip - virtually flip a coin
    * /help  - short usage description of the command
    * /hello - hello Commander. Parameter : name
    * /uptime - displays current system time
    * /shut_down - shut down socket server, use carefully

**Exemple de raspuns la fiecare comanda**

    * /dice - 5
    * /flip - Tails
    * /help  -
 	/flip - virtually flip a coin
	/uptime - displays current system time
	/hello - hello Commander. Parameter : name
	/dice - virtually role the dice
	/help -  short usage description of the command
	/shut_down - shut down socket server, use carefully

    * /hello Ana - Hello Ana! Nice to have a connection with you. 
    * /uptime - 23:32:53.396670
    * /shut_down - You finished the server session. Further commands won\'t work!
