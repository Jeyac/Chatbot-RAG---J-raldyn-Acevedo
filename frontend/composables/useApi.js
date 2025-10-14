export const useApi = () => {
  const config = useRuntimeConfig()

  const uploadDocument = async (file) => {
    const formData = new FormData()
    formData.append('archivo', file)
    
    const response = await $fetch(`${config.public.apiBase}/api/documentos/`, {
      method: 'POST',
      body: formData
    })
    
    return response
  }

  const processDocument = async (documentId) => {
    const response = await $fetch(`${config.public.apiBase}/api/documentos/${documentId}/procesar`, {
      method: 'POST'
    })
    
    return response
  }

  const getDocuments = async () => {
    const response = await $fetch(`${config.public.apiBase}/api/documentos/`)
    return response
  }

  const deleteDocument = async (documentId) => {
    try {
      const response = await $fetch(`${config.public.apiBase}/api/documentos/${documentId}`, {
        method: 'DELETE'
      })
      
      return response
    } catch (error) {
      console.error('Error eliminando documento:', error)
      throw error
    }
  }

  const getMessagesByDocument = async (documentId) => {
    const response = await $fetch(`${config.public.apiBase}/api/chat/historial/${documentId}`)
    return response
  }

  return {
    uploadDocument,
    processDocument,
    getDocuments,
    deleteDocument,
    getMessagesByDocument
  }
}
