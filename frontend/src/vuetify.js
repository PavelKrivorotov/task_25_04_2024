import 'vuetify/styles'

import { createVuetify } from 'vuetify'

import { VLayout } from 'vuetify/lib/components/index.mjs'
import { VAppBar } from 'vuetify/lib/components/index.mjs'
import { VMain } from 'vuetify/lib/components/index.mjs'
import { VContainer, VRow, VCol, VSpacer } from 'vuetify/lib/components/index.mjs'
import { VCard } from 'vuetify/lib/components/index.mjs'
import { VForm } from 'vuetify/lib/components/index.mjs'
import { VTextField } from 'vuetify/lib/components/index.mjs'
import { VSelect } from 'vuetify/lib/components/index.mjs'
import { VDataTableVirtual } from 'vuetify/lib/components/index.mjs'
import { VDialog } from 'vuetify/lib/components/index.mjs'
import { VBtn } from 'vuetify/components/VBtn'

export const vuetify = createVuetify({
    components: {
        VLayout,
        VAppBar,
        VMain,
        VContainer,
        VRow,
        VCol,
        VSpacer,
        VCard,
        VForm,
        VTextField,
        VSelect,
        VDataTableVirtual,
        VDialog,
        VBtn,
    }
})

