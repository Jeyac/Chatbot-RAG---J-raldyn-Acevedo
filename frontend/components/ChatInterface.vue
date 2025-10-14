<template>
  <div class="card p-6 h-full flex flex-col">
    <h2 class="text-xl font-semibold text-pink-800 mb-4">
      Chat con {{ documentName || 'el documento' }}
    </h2>
    
    <!-- Chat Messages Area -->
    <div 
      ref="messagesContainer"
      class="flex-1 overflow-y-auto border border-pink-200 rounded-lg p-4 mb-4 bg-gray-50 min-h-[400px] max-h-[500px]"
    >
      <div v-if="messages.length === 0" class="flex items-center justify-center h-full text-pink-500">
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-pink-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p v-if="documentId && documentName">
            Haz una pregunta sobre "{{ documentName }}"
          </p>
          <p v-else>
            Selecciona un documento para comenzar a chatear
          </p>
        </div>
      </div>
      
      <div v-else class="space-y-4">
        <div 
          v-for="message in messages" 
          :key="message.id"
          class="flex"
          :class="message.type === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div 
            class="max-w-[80%] rounded-lg px-4 py-2"
            :class="message.type === 'user' 
              ? 'bg-pink-500 text-white' 
              : 'bg-white text-gray-800 border border-pink-200'"
          >
            <div class="flex items-start space-x-2">
              <div v-if="message.type === 'bot'" class="flex-shrink-0">
                <div class="w-6 h-6 bg-pink-100 rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 text-pink-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C3.512 15.042 3 13.574 3 12c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
              <div class="flex-1">
                <p class="text-sm font-medium mb-1" v-if="message.type === 'bot'">
                  Asistente
                </p>
                <div class="whitespace-pre-wrap">{{ message.content }}</div>
                <p class="text-xs opacity-70 mt-1">
                  {{ formatTime(message.timestamp) }}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex justify-start">
          <div class="bg-white border border-pink-200 rounded-lg px-4 py-2">
            <div class="flex items-center space-x-2">
              <div class="w-6 h-6 bg-pink-100 rounded-full flex items-center justify-center">
                <svg class="w-4 h-4 text-pink-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C3.512 15.042 3 13.574 3 12c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="flex space-x-1">
                <div class="w-2 h-2 bg-pink-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Message Input -->
    <div class="flex space-x-2">
      <input 
        v-model="newMessage"
        @keydown.enter="sendMessage"
        :disabled="!isConnected || isTyping"
        placeholder="Escribe tu pregunta aquí..."
        class="input-field flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
      />
      <button 
        @click="sendMessage"
        :disabled="!newMessage.trim() || !isConnected || isTyping"
        class="btn-primary px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </div>
    
    <!-- Connection Status -->
    <div class="mt-2 flex items-center justify-between text-sm">
      <div class="flex items-center space-x-2">
        <div 
          class="w-2 h-2 rounded-full"
          :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
        ></div>
        <span :class="isConnected ? 'text-green-600' : 'text-red-600'">
          {{ isConnected ? 'Conectado' : 'Desconectado' }}
        </span>
      </div>
      <span class="text-pink-500">
        {{ messages.length }} mensajes
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  documentId: {
    type: Number,
    default: null
  },
  documentName: {
    type: String,
    default: null
  }
})

const { connect, disconnect, emit, on, off } = useSocket()
const { getMessagesByDocument } = useApi()

const messages = ref([])
const newMessage = ref('')
const isTyping = ref(false)
const isConnected = ref(false)
const messagesContainer = ref(null)

// Socket connection
onMounted(() => {
  const socket = connect()
  
  on('connect', () => {
    isConnected.value = true
  })
  
  on('disconnect', () => {
    isConnected.value = false
  })
  
  on('mensaje_recibido', (data) => {
    isTyping.value = false
    addMessage('bot', data.contenido)
  })
  
  on('error', (data) => {
    isTyping.value = false
    addMessage('bot', `Error: ${data.mensaje}`)
  })
})

onUnmounted(() => {
  disconnect()
})

// Cargar mensajes cuando cambie el documento
const loadMessagesForDocument = async () => {
  if (props.documentId) {
    try {
      const messageHistory = await getMessagesByDocument(props.documentId)
      messages.value = messageHistory.map(msg => ({
        id: msg.id,
        type: msg.es_usuario ? 'user' : 'bot',
        content: msg.contenido,
        timestamp: new Date(msg.fecha_creacion)
      }))
      scrollToBottom()
    } catch (error) {
      console.error('Error cargando mensajes del documento:', error)
    }
  } else {
    messages.value = []
  }
}

// Watcher para cargar mensajes cuando cambie el documento
watch(() => props.documentId, () => {
  loadMessagesForDocument()
}, { immediate: true })

const addMessage = (type, content) => {
  const message = {
    id: Date.now() + Math.random(),
    type,
    content,
    timestamp: new Date()
  }
  messages.value.push(message)
  scrollToBottom()
}

const sendMessage = () => {
  if (!newMessage.value.trim() || !isConnected.value || isTyping.value) return
  
  const message = newMessage.value.trim()
  newMessage.value = ''
  
  addMessage('user', message)
  isTyping.value = true
  
  emit('enviar_mensaje', {
    mensaje: message,
    documento_id: props.documentId
  })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Watch for document changes
watch(() => props.documentId, (newId) => {
  if (newId) {
    messages.value = []
    addMessage('bot', 'Documento cargado. Puedes hacer preguntas sobre su contenido.')
  }
})
</script>
