<template>
  <div class="card p-6">
    <h2 class="text-xl font-semibold text-pink-800 mb-4">
      Documentos cargados
    </h2>
    
    <div v-if="loading" class="text-center py-8">
      <svg class="animate-spin mx-auto h-8 w-8 text-black-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="text-pink-600 mt-2">Cargando documentos...</p>
    </div>
    
    <div v-else-if="documents.length === 0" class="text-center py-8 text-pink-500">
      <svg class="mx-auto h-12 w-12 text-blue-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p>No hay documentos cargados</p>
      <p class="text-sm">Sube un PDF para comenzar</p>
    </div>
    
    <div v-else class="space-y-3">
      <div 
        v-for="document in documents" 
        :key="document.id"
        class="border border-pink-200 rounded-lg p-3 hover:border-pink-300 transition-colors bg-white"
      >
        <!-- Header con icono y nombre -->
        <div class="flex items-start justify-between mb-2">
          <div class="flex items-center space-x-2 flex-1 min-w-0">
            <div class="flex-shrink-0">
              <svg class="w-6 h-6 text-pink-500" fill="currentColor" viewBox="0 0 20 20">
                <path :d="getFileIcon(document.nombre)" fill-rule="evenodd" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ document.nombre }}
              </p>
              <p class="text-xs text-gray-500">
                {{ formatFileSize(document.tamaño) }} • {{ formatDate(document.fecha_creacion) }}
              </p>
            </div>
          </div>
          
          <!-- Botón eliminar -->
          <button 
            @click="deleteDocument(document.id)"
            class="text-red-500 hover:text-red-700 p-1 flex-shrink-0"
            title="Eliminar documento"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        
        <!-- Status badges -->
        <div class="flex items-center space-x-2 mb-3">
          <span 
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
            :class="document.procesado 
              ? 'bg-green-100 text-green-800' 
              : 'bg-yellow-100 text-yellow-800'"
          >
            {{ document.procesado ? 'Procesado' : 'Pendiente' }}
          </span>
          <span 
            v-if="document.embeddings_generados"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-pink-100 text-pink-800"
          >
            Embeddings
          </span>
        </div>
        
        <!-- Botones de acción -->
        <div class="flex flex-wrap gap-2">
          <button 
            v-if="!document.procesado"
            @click="processDocument(document.id)"
            :disabled="processing === document.id"
            class="btn-primary text-xs px-3 py-1.5 disabled:opacity-50 flex-1 min-w-0"
          >
            <span v-if="processing === document.id" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-1 h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Procesando...
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Procesar
            </span>
          </button>
          
          <button 
            @click="selectDocument(document)"
            :disabled="!document.procesado"
            class="btn-secondary text-xs px-3 py-1.5 disabled:opacity-50 flex-1 min-w-0"
          >
            <span class="flex items-center justify-center">
              <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Seleccionar
            </span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Error Message -->
    <div v-if="errorMessage" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-3">
      <p class="text-red-600 text-sm">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['document-selected'])

const { getDocuments, processDocument: processDoc, deleteDocument: deleteDoc } = useApi()

const documents = ref([])
const loading = ref(false)
const processing = ref(null)
const errorMessage = ref('')

const loadDocuments = async () => {
  loading.value = true
  errorMessage.value = ''
  
  try {
    const response = await getDocuments()
    
    // El backend devuelve { documentos: [...] } pero el frontend espera directamente el array
    if (Array.isArray(response)) {
      documents.value = response
    } else if (response && response.documentos) {
      documents.value = response.documentos
    } else {
      documents.value = []
    }
  } catch (err) {
    errorMessage.value = err.data?.message || 'Error al cargar documentos'
  } finally {
    loading.value = false
  }
}

const processDocument = async (documentId) => {
  processing.value = documentId
  errorMessage.value = ''
  
  try {
    await processDoc(documentId)
    await loadDocuments() // Reload to get updated status
  } catch (err) {
    errorMessage.value = err.data?.message || 'Error al procesar documento'
  } finally {
    processing.value = null
  }
}

const deleteDocument = async (documentId) => {
  if (!confirm('¿Estás seguro de que quieres eliminar este documento? Esta acción también eliminará todo el historial de chat asociado.')) {
    return
  }
  
  errorMessage.value = ''
  
  try {
    await deleteDoc(documentId)
    await loadDocuments() // Reload to remove deleted document
  } catch (err) {
    errorMessage.value = err.data?.message || err.message || 'Error al eliminar documento'
  }
}

const selectDocument = (document) => {
  emit('document-selected', document)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible'
  
  const date = new Date(dateString)
  
  // Verificar si la fecha es válida
  if (isNaN(date.getTime())) {
    return 'Fecha inválida'
  }
  
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'America/Guatemala'
  })
}

const getFileIcon = (fileName) => {
  // Solo PDF, siempre retornar el mismo icono
  return "M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
}

// Load documents on mount
onMounted(() => {
  loadDocuments()
})

// Expose refresh method
defineExpose({
  refresh: loadDocuments
})
</script>
