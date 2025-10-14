import { io } from 'socket.io-client'

export const useSocket = () => {
  const config = useRuntimeConfig()
  let socket = null

  const connect = () => {
    if (!socket) {
      socket = io(config.public.socketUrl, {
        transports: ['websocket', 'polling'],
        autoConnect: true,
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5,
        timeout: 20000
      })
      
      socket.on('connect', () => {
        console.log('Conectado al servidor WebSocket')
      })
      
      socket.on('disconnect', (reason) => {
        console.log('Desconectado del servidor WebSocket:', reason)
      })
      
      socket.on('connect_error', (error) => {
        console.error('Error de conexión WebSocket:', error)
      })
      
      socket.on('reconnect', (attemptNumber) => {
        console.log('Reconectado al servidor WebSocket, intento:', attemptNumber)
      })
      
      socket.on('reconnect_error', (error) => {
        console.error('Error de reconexión WebSocket:', error)
      })
    }
    return socket
  }

  const disconnect = () => {
    if (socket) {
      socket.disconnect()
      socket = null
    }
  }

  const emit = (event, data) => {
    if (socket) {
      socket.emit(event, data)
    }
  }

  const on = (event, callback) => {
    if (socket) {
      socket.on(event, callback)
    }
  }

  const off = (event, callback) => {
    if (socket) {
      socket.off(event, callback)
    }
  }

  return {
    connect,
    disconnect,
    emit,
    on,
    off,
    socket: computed(() => socket)
  }
}
