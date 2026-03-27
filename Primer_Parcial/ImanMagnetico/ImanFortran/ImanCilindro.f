      PROGRAM CAMPO_B
      IMPLICIT REAL*8 (A-H,O-Z)

C=============================================================
C
C     CALCULO DEL CAMPO MAGNETICO PARA UN IMAN
C     CILINDRICO HUECO
C
C=============================================================

C     IMAX   NUMERO DE PUNTOS EN PHO
C     JMAX   NUMERO DE PUNTOS EN Z
C     PHI    ARREGLO DE DIMENSION IMAXXJMAX QUE
C            REPRESENTA EL POTENCIAL MAGNETICO
C     FLAG   ARREGLO ENTERO DE DIMENSION IMAXXJMAX QUE
C            IDENTIFICA LAS FRONTERAS DEL PROBLEMA
C     M      MAGNETIZACION (VARIABLE REAL)
C     PI     3.141592....
C     I1,J1  VERTICE INTERIOR DEL CILINDRO
C     I2,J1  VERTICE EXTERIOR DEL CILINDRO
C     V      VOLUMEN DEL IMAN

      PARAMETER (IMAX=125, JMAX=125)

      DIMENSION PHI(IMAX, JMAX)
      INTEGER FLAG(IMAX, JMAX)

      REAL*8 M
      PI = 4.D0*DATAN(1.D0)

C-------------------------------------------------------------
C     FLAG ES UN ARREGLO QUE CARACTERIZA EL PUNTO
C     EN LA MALLA. SE UTILIZA PARA DETERMINAR CUAL
C     DE LAS DIFERENTES ECUACIONES DESCRITAS
C     PERMITEN DETERMINAR LA SOLUCION.
C-------------------------------------------------------------

C     FLAG=0: PUNTO TIPICO INTERIOR.
C     FLAG=1: PUNTO TIPICO DEL BORDE INFERIOR.
C     FLAG=2: BORDE EXTERIOR SUPERIOR DE COMPUTO.
C     FLAG=3: BORDE EXTERIOR DERECHO DE COMPUTO.
C     FLAG=4: EJE DE SIMETRIA DEL IMAN.
C     FLAG=5: TAPA LATERAL INTERIOR.
C     FLAG=5: TAPA LATERAL EXTERIOR.
C     FLAG=6: TAPA SUPERIOR.
C     FLAG=7: PUNTO EN LA ESQUINA (I1,J1).
C     FLAG=7: PUNTO EN LA ESQUINA (I2,J1).

C-------------------------------------------------------------
C     PASO
C-------------------------------------------------------------

      H = 1.D0

C     POSICION DEL IMAN
      I1 = 6 * 5
      I2 = 15 * 5
      J1 = 4 * 5

C-------------------------------------------------------------
C     MAGNETIZACION
C-------------------------------------------------------------

      M = 1000.D0

C     VOLUMEN
      V = 10.D0

C-------------------------------------------------------------
C     ALPHA OPTIMO PARA COORDENADAS CARTESIANAS
C     (NO ES EL VALOR OPTIMO PARA EL PROBLEMA,
C      PERO ES UN VALOR RAZONABLE).
C-------------------------------------------------------------

      ALPHA = -1.D0 + 4.D0 /
     & (2.D0 + DSQRT(4.D0 - (DCOS(PI/IMAX) +
     & DCOS(PI/JMAX))**2))

C=============================================================
C     DEFINICION DE FLAG
C=============================================================

      DO I = 2, IMAX-1
      DO J = 2, JMAX-1
         FLAG(I,J) = 0
      END DO
      END DO

C     BORDE INFERIOR DE COMPUTO (NO CAMBIA)
      DO I = 1, IMAX
         FLAG(I,1) = 1
      END DO

C     BORDE SUPERIOR DE COMPUTO (NO CAMBIA)
      DO I = 1, IMAX
         FLAG(I,JMAX) = 2
      END DO

C     BORDE DERECHO DE COMPUTO (NO CAMBIA)
      DO J = 2, JMAX-1
         FLAG(IMAX,J) = 3
      END DO

C     EJE DE SIMETRIA
      DO J = 2, JMAX-1
         FLAG(1,J) = 4
      END DO

C     TAPAS LATERALES
      DO J = 2, J1-1
         FLAG(I1,J) = 5
         FLAG(I2,J) = 5
      END DO

C     TAPA SUPERIOR
      DO I = I1+1, I2-1
         FLAG(I,J1) = 6
      END DO

C     PUNTOS DEL BORDE
      FLAG(I1,J1) = 7
      FLAG(I2,J1) = 7

C=============================================================
C     INICIALIZACION DE PHI
C=============================================================

      DO I = 1, IMAX
      DO J = 1, JMAX
         PHI(I,J) = 1.D0
      END DO
      END DO

C     ESTOS VALORES NO CAMBIAN EN EL CALCULO

      DO I = 1, IMAX
         PHI(I,1) = 0.D0
      END DO

      DO I = 1, IMAX
         PHI(I,JMAX) = V*M/(4.D0*PI*(I*H)**3)
      END DO

      DO J = 1, JMAX
         PHI(IMAX,J) = V*M/(4.D0*PI*(IMAX*H)**3)
      END DO

C=============================================================
C     SOLUCION POR EL METODO DE SOBRERELAJACION
C=============================================================

      DO ICOUNT = 1, 200
      DO I = 1, IMAX-1
      DO J = 1, JMAX-1

         IF (FLAG(I,J) .EQ. 0) THEN

            A = 1.D0 + 1.D0/2.D0/FLOAT(I)
            B = 1.D0 - 1.D0/2.D0/FLOAT(I)

            NUEVO = (A*PHI(I+1,J) + B*PHI(I-1,J)
     &              + PHI(I,J+1) + PHI(I,J-1)) / 4.D0

         ELSE IF (FLAG(I,J).EQ.1 .OR.
     &            FLAG(I,J).EQ.2 .OR.
     &            FLAG(I,J).EQ.3) THEN

            NUEVO = PHI(I,J)

         ELSE IF (FLAG(I,J).EQ.4) THEN

            NUEVO = (4.D0*PHI(2,J) + PHI(1,J+1)
     &               + PHI(1,J-1)) / 6.D0

         ELSE IF (FLAG(I,J).EQ.5) THEN

            NUEVO = (PHI(I+1,J) + PHI(I-1,J)) / 2.D0

         ELSE IF (FLAG(I,J).EQ.6) THEN

            NUEVO = (M*H + PHI(I,J+1)
     &               + PHI(I,J-1)) / 2.D0

         ELSE IF (FLAG(I,J).EQ.7) THEN

            NUEVO = (M*H + PHI(I,J+1) + PHI(I,J-1)
     &               + PHI(I+1,J) + PHI(I-1,J)) / 4.D0

         ELSE
            STOP 'EL PUNTO DE LA REGION NO ESTA INDEXADO!'
         ENDIF

         PHI(I,J) = NUEVO + ALPHA*(NUEVO - PHI(I,J))

      END DO
      END DO
      END DO

C=============================================================
C     SALIDA POTENCIAL
C=============================================================

      OPEN(10, FILE='POT-MAG')

      DO I = 1, IMAX
      DO J = 1, JMAX
         WRITE(10,*) I, J, PHI(I,J)
      END DO
         WRITE(10,'()')
      END DO

      CLOSE(10)

C=============================================================
C     CAMPO H
C=============================================================

      OPEN(10, FILE='CAMPO-H')

      DO I = 2, IMAX-1, 5
      DO J = 2, JMAX-1, 5
         WRITE(10,*) I, J,
     &      (PHI(I+1,J)-PHI(I-1,J))/H/2.D0,
     &      (PHI(I,J+1)-PHI(I,J-1))/H/2.D0
      END DO
         WRITE(10,'()')
      END DO

      CLOSE(10)

C=============================================================
C     CAMPO B
C=============================================================

      OPEN(11, FILE='CAMPO-B')

      DO I = 2, IMAX-1, 5
      DO J = 2, JMAX-1, 5

         AA = 0.D0
         IF (I.GE.I1 .AND. I.LE.I2 .AND. J.LE.J1) AA = M

         WRITE(11,*) I, J,
     &      -(PHI(I+1,J)-PHI(I-1,J))/H/2.D0,
     &      AA - (PHI(I,J+1)-PHI(I,J-1))/H/2.D0

      END DO
         WRITE(11,'()')
      END DO

      CLOSE(11)

      END