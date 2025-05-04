plugins {
    kotlin("jvm") version "1.8.10"
}

group = "com.example"
version = "1.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))

    testImplementation("org.junit.jupiter:junit-jupiter-api:5.10.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.10.0")
}

tasks.register<Exec>("runLocust") {
    group = "verification"
    description = "Run Locust load test"

    commandLine("locust", "-f", "locustfile.py", "--host=http://your-app-url.com", "--headless", "--users=10000", "--spawn-rate=100")
}

tasks.register<Exec>("runLocustTest") {
    group = "verification"
    description = "Run Locust load test with 10k users"

    environment("JWT_SECRET", "development_secret_key")
    environment("JWT_AUDIENCE", "mad-mobile-app")

    commandLine(
        "locust", "-f", "locustfile.py", "--headless",
        "--users=10000", "--spawn-rate=100", "--host=http://188.225.77.13"
    )
}


tasks.withType<Test> {
    useJUnitPlatform()
}
