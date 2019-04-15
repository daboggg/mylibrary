package ru.zinin.mylibrary.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import ru.zinin.mylibrary.domain.User;
import ru.zinin.mylibrary.repos.UserRepo;

@Service
public class UserService implements UserDetailsService {

    @Autowired
    private UserRepo userRepo;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return userRepo.findByUsername(username);
    }

    public void updateProfile(String password, User user) {
        if (!user.getPassword().equals(password)) {
            user.setPassword(password);
            userRepo.save(user);
        }
    }
}
