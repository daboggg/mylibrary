package ru.zinin.mylibrary.repos;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.zinin.mylibrary.domain.User;

public interface UserRepo extends JpaRepository<User, Long> {
    User findByUsername(String username);
}
