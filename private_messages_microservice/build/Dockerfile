FROM golang:1.23.3-alpine3.20 as builder

LABEL meintainer="LedxDeliveryFlopp"

WORKDIR /builds

COPY . .

RUN go mod download && go mod tidy && go build -o /api cmd/api/main.go

FROM scratch

WORKDIR /app

COPY --from=builder api/ /app/api

ENTRYPOINT ["/app/api"]

#ENTRYPOINT ["tail", "-f", "/dev/null"]