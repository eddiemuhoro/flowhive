declare module "vue-pdf-embed" {
  import { DefineComponent } from "vue";

  interface VuePdfEmbedProps {
    source?: string | ArrayBuffer | Uint8Array;
    page?: number;
    scale?: number;
    rotation?: number;
    width?: number;
    height?: number;
  }

  const VuePdfEmbed: DefineComponent<VuePdfEmbedProps>;
  export default VuePdfEmbed;
}
