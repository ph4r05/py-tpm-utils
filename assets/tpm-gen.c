/* gcc -Wall -O2 -ltspi -o tpm-getrand tpm-getrand.c
 *
 * Usage:
 * ./tpm-getrand | dd of=/tmp/random.data count=10 bs=1k
 *
 * Get random bytes from TPM pRNG
 *
 * Copyright (C) 2009 Kees Cook <kees@outflux.net>
 * http://outflux.net/tpm/tpm-getrand.c
 * License: GPLv3
 *
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <inttypes.h>

#include <trousers/tss.h>
#include <trousers/trousers.h>

int main(int argc, char * argv[])
{
    int size = 1024;
    BYTE *bytes;
    TSS_RESULT rc;
    TSS_HCONTEXT hContext;
    TSS_HTPM hTPM;


    if ((rc=Tspi_Context_Create(&hContext)) != TSS_SUCCESS) {
        fprintf(stderr,"Tspi_Context_Create: %s\n", Trspi_Error_String(rc));
        return 1;
    }

    if ((rc=Tspi_Context_Connect(hContext, NULL)) != TSS_SUCCESS) {
        fprintf(stderr,"Tspi_Context_Connect: %s\n", Trspi_Error_String(rc));
        return 2;
    }

    if ((rc=Tspi_Context_GetTpmObject(hContext, &hTPM)) != TSS_SUCCESS) {
        fprintf(stderr,"Tspi_Context_GetTpmObject: %s\n", Trspi_Error_String(rc));
        return 3;
    }

    for(;;){
      if ((rc=Tspi_TPM_GetRandom(hTPM, size, &bytes)) != TSS_SUCCESS) {
          fprintf(stderr,"Tspi_TPM_GetRandom: %s\n", Trspi_Error_String(rc));
          return 4;
      }

      fwrite(bytes, size, 1, stdout);
      Tspi_Context_FreeMemory(hContext, bytes);
    }

    Tspi_Context_Close(hContext);
    return 0;
}
