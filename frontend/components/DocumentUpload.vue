<template>
  <div class="card shadow-sm border-0">
    <div class="card-header bg-transparent border-0 pb-0">
      <h2 class="card-title text-lg font-semibold text-pink-800 mb-0 d-flex align-items-center">
        <i class="bi bi-cloud-upload me-2"></i>
        Subir documento
      </h2>
    </div>
    <div class="card-body p-4">
    
    <div class="space-y-4">
      <!-- Upload Area -->
      <div 
        class="border-2 border-dashed border-pink-300 rounded-3 p-4 text-center hover:border-pink-400 transition-all cursor-pointer position-relative"
        @click="triggerFileInput"
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <div v-if="!selectedFile" class="space-y-2">
          <svg class="mx-auto h-10 w-10 text-pink-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <p class="text-sm text-pink-600">Arrastra tu documento PDF aquí o haz clic para seleccionar</p>
          <p class="text-xs text-pink-400">Solo archivos PDF (hasta 10MB)</p>
        </div>
        
        <div v-else class="space-y-2">
          <i class="bi bi-file-earmark-pdf text-success" style="font-size: 2.5rem;"></i>
          <p class="text-sm text-success fw-medium">{{ selectedFile.name }}</p>
          <p class="text-xs text-muted">{{ formatFileSize(selectedFile.size) }}</p>
        </div>
      </div>
      
        <input 
          ref="fileInput"
          type="file" 
          accept=".pdf"
          @change="handleFileSelect"
          class="hidden"
        />
      
      <!-- Upload Button -->
      <button 
        v-if="selectedFile"
        @click="uploadFile"
        :disabled="uploading"
        class="btn btn-primary w-100 d-flex align-items-center justify-content-center"
      >
        <span v-if="uploading" class="d-flex align-items-center">
          <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          Subiendo...
        </span>
        <span v-else class="d-flex align-items-center">
          <i class="bi bi-upload me-2"></i>
          Subir documento
        </span>
      </button>
      
      <!-- Error Message -->
      <div v-if="error" class="alert alert-danger d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        <div>{{ error }}</div>
      </div>
      
      <!-- Success Message -->
      <div v-if="success" class="alert alert-success d-flex align-items-center" role="alert">
        <i class="bi bi-check-circle-fill me-2"></i>
        <div>{{ success }}</div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['document-uploaded'])

const fileInput = ref(null)
const selectedFile = ref(null)
const uploading = ref(false)
const error = ref('')
const success = ref('')

const { uploadDocument } = useApi()

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const validateAndSetFile = (file) => {
  error.value = ''
  success.value = ''
  
  // Validar extensión del archivo (solo PDF)
  const fileName = file.name.toLowerCase()
  
  if (!fileName.endsWith('.pdf')) {
    error.value = 'Solo se permiten archivos PDF'
    return
  }
  
  if (file.size > 10 * 1024 * 1024) { // 10MB
    error.value = `El archivo no puede ser mayor a 10MB. Tamaño actual: ${(file.size / (1024*1024)).toFixed(2)}MB`
    return
  }
  
  selectedFile.value = file
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await uploadDocument(selectedFile.value)
    success.value = 'Documento subido exitosamente'
    emit('document-uploaded', response)
    
    // Reset form
    selectedFile.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  } catch (err) {
    error.value = err.data?.message || 'Error al subir el documento'
  } finally {
    uploading.value = false
  }
}
</script>
