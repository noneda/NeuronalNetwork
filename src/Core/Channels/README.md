# **WEBSOCKET CORE**

## **🎯 Uso de Decoradores para WebSocket**

```python
# Crear router
ws_router = WebSocketRouter()

# Definir eventos con decoradores
@ws_router.on('message')
def handle_message(msg: WebSocketMessage):
    """Maneja mensajes de chat"""
    text = msg.data.get('text')
    username = msg.handler.client_data.get('username', 'Anonymous')
    
    # Broadcast a todos los clientes
    msg.broadcast('new_message', {
        'username': username,
        'text': text
    })

@ws_router.on('join')
def handle_join(msg: WebSocketMessage):
    """Usuario se une"""
    username = msg.data['username']
    msg.handler.client_data['username'] = username
    
    msg.broadcast('user_joined', {
        'username': username
    }, include_self=True)
```

## **✨ Características principales:**

### **1. Decorador de eventos**
```python
@ws_router.on('nombre_evento')
def handler(msg: WebSocketMessage):
    # Tu lógica aquí
    pass
```

### **2. Objeto WebSocketMessage**
```python
def handler(msg: WebSocketMessage):
    msg.data           # Data parseada del JSON
    msg.text           # Texto raw del mensaje
    msg.event          # Nombre del evento
    msg.client_ip      # IP del cliente
    msg.client_port    # Puerto del cliente
    msg.handler        # Acceso al handler del cliente
```

### **3. Emitir mensajes**
```python
# Enviar al cliente que envió el mensaje
msg.emit('response', {'status': 'ok'})

# Broadcast a TODOS (incluyendo el remitente)
msg.broadcast('notification', {'text': 'Hola a todos'}, include_self=True)

# Broadcast a TODOS excepto el remitente
msg.broadcast('notification', {'text': 'Otro usuario hizo algo'}, include_self=False)
```

### **4. Middlewares globales**
```python
@ws_router.use
def log_middleware(msg: WebSocketMessage):
    """Se ejecuta antes de cada evento"""
    Logger.log(f"Evento: {msg.event}")
    return True  # True = continuar, False = bloquear

@ws_router.use
def auth_middleware(msg: WebSocketMessage):
    """Requiere autenticación"""
    if not msg.handler.client_data.get('authenticated'):
        msg.emit('error', {'message': 'No autenticado'})
        return False  # Bloquea el evento
    return True
```

### **5. Datos del cliente persistentes**
```python
@ws_router.on('login')
def handle_login(msg: WebSocketMessage):
    username = msg.data['username']
    
    # Guardar en el handler del cliente
    msg.handler.client_data['username'] = username
    msg.handler.client_data['authenticated'] = True
    
    msg.emit('login_success', {'username': username})

@ws_router.on('message')
def handle_message(msg: WebSocketMessage):
    # Acceder a datos guardados
    username = msg.handler.client_data.get('username', 'Anonymous')
    # ...
```

## **📡 Formato de mensajes (Cliente ↔ Servidor)**

**Cliente envía:**
```javascript
// JavaScript en el navegador
const ws = new WebSocket('ws://localhost:8765');

// Enviar evento
ws.send(JSON.stringify({
    event: 'message',
    data: {
        text: 'Hola mundo',
        timestamp: Date.now()
    }
}));

// Recibir eventos
ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    console.log(msg.event, msg.data);
    // msg = { event: 'new_message', data: {...} }
};
```

**Servidor responde:**
```python
msg.emit('response', {'status': 'ok'})
# Envía: {"event": "response", "data": {"status": "ok"}}
```

## **🎮 Ejemplo completo de uso:**

```python
# Crear router
ws_router = WebSocketRouter()

# Middlewares
@ws_router.use
def log_events(msg):
    Logger.log(f"[{msg.event}] from {msg.client_ip}")
    return True

# Eventos para juego multiplayer
@ws_router.on('player_move')
def handle_move(msg: WebSocketMessage):
    """Jugador se mueve"""
    x = msg.data['x']
    y = msg.data['y']
    player_id = msg.handler.client_data['player_id']
    
    # Broadcast posición a otros jugadores
    msg.broadcast('player_moved', {
        'player_id': player_id,
        'x': x,
        'y': y
    }, include_self=False)

@ws_router.on('attack')
def handle_attack(msg: WebSocketMessage):
    """Jugador ataca"""
    target_id = msg.data['target_id']
    damage = msg.data['damage']
    
    # Buscar jugador objetivo
    for client in ws_router.clients:
        if client.client_data.get('player_id') == target_id:
            client.emit('receive_damage', {
                'damage': damage,
                'from': msg.handler.client_data['player_id']
            })
            break

@ws_router.on('chat')
def handle_chat(msg: WebSocketMessage):
    """Chat del juego"""
    msg.broadcast('chat_message', {
        'player': msg.handler.client_data['player_name'],
        'text': msg.data['text']
    }, include_self=True)
```

## **🔌 Cliente HTML de prueba:**

```html
<!DOCTYPE html>
<html>
<body>
    <input id="username" placeholder="Username">
    <button onclick="join()">Join</button>
    <input id="message" placeholder="Message">
    <button onclick="send()">Send</button>
    <div id="messages"></div>

    <script>
        const ws = new WebSocket('ws://localhost:8765');
        
        ws.onmessage = (e) => {
            const msg = JSON.parse(e.data);
            console.log(msg.event, msg.data);
            
            if (msg.event === 'new_message') {
                document.getElementById('messages').innerHTML += 
                    `<p><b>${msg.data.username}:</b> ${msg.data.text}</p>`;
            }
        };
        
        function join() {
            const username = document.getElementById('username').value;
            ws.send(JSON.stringify({
                event: 'join',
                data: { username }
            }));
        }
        
        function send() {
            const text = document.getElementById('message').value;
            ws.send(JSON.stringify({
                event: 'message',
                data: { text, timestamp: Date.now() }
            }));
            document.getElementById('message').value = '';
        }
    </script>
</body>
</html>
```
