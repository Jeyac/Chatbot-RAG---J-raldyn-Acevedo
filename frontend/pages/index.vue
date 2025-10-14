<template>
  <div class="min-h-screen bg-pink-50 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <div class="mx-auto h-16 w-16 bg-pink-500 rounded-full flex items-center justify-center mb-4">
          <svg class="h-8 w-8 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-pink-800">Seven (707)</h2>
        <p class="mt-2 text-sm text-pink-600">
          Sistema de preguntas y respuestas con Seven, tu asistente virtual de confianza
        </p>
      </div>
      
      <div class="bg-white py-8 px-6 shadow rounded-lg border border-pink-200">
        <div class="space-y-4">
          <div class="text-center">
            <h3 class="text-lg font-medium text-pink-800 mb-2">
              ¡Bienvenido soy Seven, tu asistente virtual!
            </h3>
            <p class="text-sm text-pink-600 mb-6">
              Sube un documento PDF y haz preguntas sobre su contenido.
            </p>
          </div>
          
          <div class="space-y-3">
            <div class="flex items-center space-x-3 text-sm text-pink-600">
              <svg class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Sube documentos PDF</span>
            </div>
            <div class="flex items-center space-x-3 text-sm text-pink-600">
              <svg class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Procesa con IA</span>
            </div>
            <div class="flex items-center space-x-3 text-sm text-pink-600">
              <svg class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Haz preguntas en tiempo real</span>
            </div>
          </div>
          
          <div class="pt-4">
            <NuxtLink 
              to="/chatbot" 
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-pink-500 hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 transition-colors duration-200"
            >
              Comenzar
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <div class="text-center">
        <p class="text-xs text-pink-500">
          Desarrollado por Jéralyn Acevedo
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Meta tags para SEO
useHead({
  title: 'Seven (707)',
  meta: [
    { name: 'description', content: 'Sistema inteligente de preguntas y respuestas basado en documentos PDF' }
  ]
})
</script>
