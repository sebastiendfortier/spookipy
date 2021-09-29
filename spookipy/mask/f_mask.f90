! FMASK

SUBROUTINE F_MASK(SLAB, NI, NJ, VALUES, OPERATORS, THRESHOLDS, N)

IMPLICIT NONE
INTEGER,  INTENT(IN)   :: NI
INTEGER,  INTENT(IN)   :: NJ
INTEGER,  INTENT(IN)   :: N
real,     intent(inout):: SLAB(NI ,NJ)
REAL,     INTENT(IN)   :: VALUES(N)
INTEGER,  INTENT(IN)   :: OPERATORS(N)
REAL,     INTENT(IN)   :: THRESHOLDS(N)

INTEGER I, J, K
REAL TMP

    DO J=1, NJ
        DO I=1, NI
            TMP = SLAB(I,J)
            SLAB(I,J) = 0.
            INNER: DO K=1, N
                IF (OPERATORS(K) .EQ. 0) THEN ! >
                    IF (TMP .GT. THRESHOLDS(K)) THEN
                        SLAB(I,J) = VALUES(K)
                        EXIT INNER
                    ENDIF
                ELSEIF (OPERATORS(K) .EQ. 1) THEN ! >=
                    ! print *,OPERATORS(K),TMP,THRESHOLDS(K),VALUES(K),(TMP .GE. THRESHOLDS(K))
                    IF (TMP .GE. THRESHOLDS(K)) THEN
                        SLAB(I,J) = VALUES(K)
                        EXIT INNER
                    ENDIF
                ELSEIF (OPERATORS(K) .EQ. 2) THEN ! ==
                    IF ((TMP.GE. (THRESHOLDS(K) - 0.4)) .AND. (TMP .LE. (THRESHOLDS(K) + 0.4))) THEN ! IF (TMP >= (T - 0.4) ) AND (TMP <= (T + 0.4)):
                        SLAB(I,J) = VALUES(K)
                        EXIT INNER
                    ENDIF
                ELSEIF (OPERATORS(K) .EQ. 3) THEN ! <=
                    IF (TMP .LE. THRESHOLDS(K)) THEN
                        SLAB(I,J) = VALUES(K)
                        EXIT INNER
                    ENDIF
                ELSEIF (OPERATORS(K) .EQ. 4) THEN ! <
                    IF (TMP .LT. THRESHOLDS(K)) THEN
                        SLAB(I,J) = VALUES(K)
                        EXIT INNER
                    ENDIF
                ELSE ! IF (OPERATORS(K) .EQ. 5) THEN ! !=
                    IF (TMP .NE. THRESHOLDS(K)) THEN
                        SLAB(I,J) = VALUES(K)
                        EXIT INNER
                    ENDIF
                ENDIF
            ENDDO INNER
        ENDDO
    ENDDO

END SUBROUTINE F_MASK
