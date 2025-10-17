<template>
  <div class="min-h-screen bg-pink-50">
    <!-- Header de la aplicación -->
    <header class="bg-white shadow-sm border-b border-pink-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">

          <!-- Logo e información del asistente -->
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-pink-500 rounded-lg flex items-center justify-center">
              <!-- Icono del asistente -->
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-pink-800">Seven tu asistente virtual</h1>
              <p class="text-sm text-pink-600">Sistema de preguntas y respuestas</p>
            </div>
          </div>
          
          <!-- Estado de conexión WebSocket -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <!-- Indicador visual -->
              <div 
                class="w-2 h-2 rounded-full"
                :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
              ></div>
              <span class="text-sm" :class="isConnected ? 'text-green-600' : 'text-red-600'">
                {{ isConnected ? 'Conectado' : 'Desconectado' }}
              </span>
            </div>
          </div>

        </div>
      </div>
    </header>
    
    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <!-- Columna izquierda: Gestión de documentos -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Componente para subir documentos -->
          <DocumentUpload @document-uploaded="handleDocumentUploaded" />

          <!-- Lista de documentos existentes -->
          <DocumentList 
            ref="documentList"
            @document-selected="handleDocumentSelected" 
          />
        </div>
        
        <!-- Columna derecha: Interfaz de chat -->
        <div class="lg:col-span-2">
          <ChatInterface 
            :document-id="selectedDocument?.id"
            :document-name="selectedDocument?.nombre"
          />
        </div>

      </div>
    </main>
    
    <!-- Footer -->
    <footer class="bg-white border-t border-pink-200 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="text-center text-sm text-pink-500">
          <p>Chatbot RAG - Sistema de preguntas y respuestas con IA</p>
          <p class="mt-1">Desarrollado con Nuxt 3, Flask y OpenAI</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Metadata SEO para la página
useHead({
  title: 'Seven tu asistente virtual, te ayuda a consultar tus archivos',
  meta: [
    { name: 'description', content: 'Sistema inteligente de preguntas y respuestas basado en documentos PDF' },
    { name: 'keywords', content: 'chatbot, RAG, IA, preguntas, respuestas, PDF, OpenAI' }
  ]
})

// Importa el hook personalizado para manejar WebSockets
const { connect, disconnect, on, off } = useSocket()

// Referencias y estados reactivos
const documentList = ref(null)         // Referencia al componente DocumentList
const selectedDocument = ref(null)     // Documento actualmente seleccionado
const isConnected = ref(false)         // Estado de conexión WebSocket

// Conexión a WebSocket al montar el componente
onMounted(() => {
  const socket = connect()
  
  on('connect', () => {
    isConnected.value = true
  })
  
  on('disconnect', () => {
    isConnected.value = false
  })
})

// Desconectar WebSocket al desmontar el componente
onUnmounted(() => {
  disconnect()
})

// Maneja evento de documento subido
const handleDocumentUploaded = (document) => {
  // Actualiza la lista de documentos
  if (documentList.value) {
    documentList.value.refresh()
  }
}

// Maneja selección de documento desde la lista
const handleDocumentSelected = (document) => {
  selectedDocument.value = document
}
</script>
